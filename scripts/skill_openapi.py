#!/usr/bin/env python3
"""Generate and verify the installed skill's pinned OpenAPI bindings."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shlex
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit, parse_qsl

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/omneity'
SOURCE_URL = 'https://api.sawalni.com/openapi.json'
HTTP_METHODS = {'get','post','put','patch','delete','head','options','trace'}
FENCES = re.compile(r'(?P<annotation><!-- api-example: (?P<operation>\S+) (?P<media>\S+) -->\n)?```(?P<language>json|bash)\n(?P<body>.*?)\n```', re.S)
ENDPOINT = re.compile(r'\b(GET|POST|PUT|DELETE|PATCH) (/v1/[^\s`?,\'\"]+|/api/public/[^\s`?,\'\"]+)')


def encode(value):
    return json.dumps(value, ensure_ascii=False, indent=2)+'\n'


def operations(spec):
    result = {}
    for path, methods in spec['paths'].items():
        for method, operation in methods.items():
            if method not in HTTP_METHODS:
                continue
            key = operation['operationId']
            if key in result:
                raise ValueError('Duplicate operationId: '+key)
            result[key] = (method, path, operation)
    return result


def resolve(spec, schema):
    if '$ref' not in schema:
        return schema
    pointer = schema['$ref']
    if not pointer.startswith('#/'):
        raise ValueError('Only bundled local schema references are supported')
    value = spec
    for key in pointer[2:].split('/'):
        value = value[key.replace('~1','/').replace('~0','~')]
    return {**resolve(spec,value), **{k:v for k,v in schema.items() if k!='$ref'}}


def describe(schema):
    if 'oneOf' in schema:
        return ' or '.join(describe(part) for part in schema['oneOf'])
    kind = schema.get('type', 'object')
    if isinstance(kind,list):
        return ' or '.join(kind)
    return describe(schema.get('items',{}))+'[]' if kind=='array' else kind


def limits(schema):
    result = []
    for key in ['default','enum','const','minimum','maximum','minLength','maxLength','minItems','maxItems','pattern']:
        if key in schema:
            result.append(key+'='+json.dumps(schema[key],ensure_ascii=False))
    if schema.get('description'):
        result.append(schema['description'])
    return '; '.join(result).replace('|','\\|').replace('\n',' ')


def generated(spec, skill=SKILL):
    bindings = json.loads((skill/'references/api-bindings.json').read_text())
    if bindings['source_url'] != SOURCE_URL:
        raise ValueError('Unexpected public specification URL')
    raw = encode(spec)
    digest = hashlib.sha256(raw.encode()).hexdigest()
    result = {skill/'references/openapi.json': raw,
              skill/'references/openapi-lock.json':encode({'source_url':SOURCE_URL,'sha256':digest,'spec_version':spec['info']['version'],'http_operations':len(operations(spec))})}
    registry = operations(spec)
    for filename, binding in bindings['references'].items():
        if Path(filename).name!=filename or not filename.endswith('.md'):
            raise ValueError('Invalid skill reference filename')
        rows = ['# API contract: '+Path(filename).stem, '', 'Generated from the pinned public OpenAPI file. Do not edit.', '', f'Source: [{SOURCE_URL}]({SOURCE_URL}).', '', 'Use the companion task reference for workflow guidance.', '']
        for opid in binding['operations']:
            if opid not in registry:
                raise ValueError(filename+': unknown operationId '+opid)
            method,path,op=registry[opid]
            security=op.get('security',spec.get('security',[]))
            auth='; '.join(' + '.join(item) for item in security) or 'No authentication'
            rows += ['## '+opid,'',f'`{method.upper()} {path}`','',op['summary'],'','Authentication: `'+auth+'`.','']
            for media, value in op.get('requestBody',{}).get('content',{}).items():
                schema=resolve(spec,value['schema'])
                rows += ['Request content type: `'+media+'`.','','| Field | Type | Required | Constraints and defaults |','|---|---|---|---|']
                for field,prop in schema.get('properties',{}).items():
                    prop=resolve(spec,prop)
                    rows.append(f"| `{field}` | {describe(prop)} | {'yes' if field in schema.get('required',[]) else 'no'} | {limits(prop)} |")
                if 'oneOf' in schema:
                    rows += ['', 'Request alternatives: `'+json.dumps(schema['oneOf'],ensure_ascii=False)+'`.']
                if 'example' in value:
                    rows += ['','Example from the contract:','','```json',json.dumps(value['example'],ensure_ascii=False,indent=2),'```']
                rows.append('')
            parameters=op.get('parameters',[])
            if parameters:
                rows += ['| Parameter | Location | Type | Required | Constraints and defaults |','|---|---|---|---|---|']
                for param in parameters:
                    schema=resolve(spec,param['schema'])
                    rows.append(f"| `{param['name']}` | {param['in']} | {describe(schema)} | {'yes' if param.get('required') else 'no'} | {limits(schema)} |")
                rows.append('')
            for status,response in op['responses'].items():
                if status.startswith('2'):
                    rows.append('Success: `'+status+'`; content types: '+', '.join('`'+v+'`' for v in response.get('content',{})) +'.')
            if op.get('description'):
                rows += ['',op['description']]
            rows.append('')
        for path in binding.get('websockets',[]):
            ws=spec['x-websocket'][path]
            rows += ['## WebSocket '+path,'','This is a published OpenAPI extension, not an HTTP operation.','','```json',json.dumps(ws,ensure_ascii=False,indent=2),'```','']
        result[skill/'references/contracts'/(Path(filename).stem+'.md')]='\n'.join(rows)
    return result


def validate_body(spec, schema, payload):
    from jsonschema import Draft202012Validator
    # OpenAPI may allow extra API fields. Documentation examples must use named
    # contract fields so misspellings are not silently accepted.
    resolved=resolve(spec,schema)
    if isinstance(payload,dict) and resolved.get('properties') and resolved.get('additionalProperties') is not True:
        unknown=set(payload)-set(resolved['properties'])
        if unknown:
            raise ValueError('Undocumented request fields: '+', '.join(sorted(unknown)))
    wrapped={**schema,'components':spec['components']}
    Draft202012Validator(wrapped).validate(payload)


def convert_query(schema, value):
    kind=schema.get('type')
    if kind=='integer': return int(value)
    if kind=='number': return float(value)
    if kind=='boolean':
        if value not in {'true','false'}:raise ValueError('Expected true or false query value')
        return value=='true'
    return value


def validate_query(spec, op, values):
    from jsonschema import Draft202012Validator
    params={p['name']:p for p in op.get('parameters',[]) if p['in']=='query'}
    unknown=set(values)-set(params)
    if unknown:raise ValueError('Undocumented query fields: '+', '.join(sorted(unknown)))
    for name,param in params.items():
        if param.get('required') and name not in values:raise ValueError('Missing query parameter '+name)
        if name in values:
            schema=resolve(spec,param['schema'])
            Draft202012Validator(schema).validate(convert_query(schema,values[name]))


def parse_curl(body):
    tokens=shlex.split(body.replace('\\\n',''))
    if not tokens or tokens.pop(0)!='curl':raise ValueError('Expected one curl request example')
    method=None;url=None;data=[];form={};query={};has_get=False
    while tokens:
        token=tokens.pop(0)
        if token in {'--get','-G'}:has_get=True;continue
        if token in {'-s','-sS','--silent','--fail'}:continue
        if token.startswith('https://'):url=token;continue
        if token in {'-H','--header','-X','--request','-d','--data','--data-raw','--data-urlencode','-F','--form'}:
            value=tokens.pop(0)
            if token in {'-X','--request'}:method=value.lower()
            elif token in {'-H','--header'}:pass
            elif token in {'-F','--form'}:
                key,value=value.split('=',1);form[key]=value
            else:data.append(value)
            continue
        raise ValueError('Unsupported curl example token: '+token)
    if not url:raise ValueError('Missing curl URL')
    parts=urlsplit(url)
    if parts.scheme!='https' or parts.netloc!='api.sawalni.com':raise ValueError('Unexpected API example host')
    query=dict(parse_qsl(parts.query))
    if has_get:
        for value in data:
            key,value=value.split('=',1);query[key]=value
    payload=form or (json.loads(data[0]) if data and not has_get else None)
    return method or ('get' if has_get or not(data or form) else 'post'),parts.path,query,payload


def validate_example(spec, binding, operation, media, language, body):
    if operation.startswith('ws:'):
        path=operation[3:]
        if path not in binding.get('websockets',[]) or media!='start' or language!='json':raise ValueError('Unbound WebSocket example')
        payload=json.loads(body); expected=spec['x-websocket'][path]['start']
        if set(payload)!=set(expected):raise ValueError('WebSocket start fields differ from contract')
        for name,value in expected.items():
            if name in {'model','language'}:
                if not isinstance(payload[name],str):raise ValueError('Invalid WebSocket '+name)
            elif payload[name]!=value:raise ValueError('Invalid WebSocket '+name)
        return
    if operation not in binding['operations']:raise ValueError('Example is not bound to this task reference')
    method,path,op=operations(spec)[operation]
    if language=='bash':
        actual_method,actual_path,query,payload=parse_curl(body)
        if actual_method!=method or not re.fullmatch(re.sub(r'\{[^}]+\}',r'[^/]+',path),actual_path):raise ValueError('curl method/path differs from annotated operation')
        validate_query(spec,op,query)
    else:
        payload=json.loads(body)
        if media=='query':
            validate_query(spec,op,payload);return
    if media=='query':
        if payload is not None:raise ValueError('GET query example has an unexpected body')
        return
    content=op.get('requestBody',{}).get('content',{})
    if media not in content:raise ValueError('Undocumented request content type '+media)
    validate_body(spec,content[media]['schema'],payload)


def lint_skill(spec, skill=SKILL):
    from jsonschema import ValidationError
    bindings=json.loads((skill/'references/api-bindings.json').read_text())
    registry=operations(spec); covered=set();websockets=set();examples=0
    for path,expected in generated(spec,skill).items():
        if not path.exists() or path.read_text()!=expected:raise ValueError('Stale skill artifact: '+str(path.relative_to(skill)))
    expected_contracts={Path(name).stem+'.md' for name in bindings['references']}
    existing_contracts={file.name for file in (skill/'references/contracts').glob('*.md')}
    if existing_contracts!=expected_contracts:raise ValueError('Unexpected or missing generated contract files')
    if (skill/'references/openapi.json').read_bytes()!=encode(spec).encode():raise ValueError('Bundled specification differs')
    for filename,binding in bindings['references'].items():
        file=skill/'references'/filename; text=file.read_text()
        link='contracts/'+Path(filename).stem+'.md'
        if ']('+link+')' not in text:raise ValueError(filename+': missing generated contract link')
        for op in binding['operations']:
            if op not in registry:raise ValueError(filename+': unknown operation '+op)
            covered.add(op)
        for path in binding.get('websockets',[]):
            if path not in spec.get('x-websocket',{}):raise ValueError('Unknown WebSocket '+path)
            websockets.add(path)
        for match in FENCES.finditer(text):
            if not match['annotation']:raise ValueError(filename+': unbound '+match['language']+' example')
            try:validate_example(spec,binding,match['operation'],match['media'],match['language'],match['body'])
            except (ValueError,ValidationError,KeyError,IndexError) as exc:raise ValueError(filename+': '+str(exc)) from exc
            examples+=1
        for method,path in ENDPOINT.findall(text):
            normalize=lambda value:re.sub(r'\{[^}]+\}','{}',value)
            if not any(m==method.lower() and normalize(p)==normalize(path) for opid,(m,p,op) in registry.items() if opid in binding['operations']):raise ValueError(filename+': endpoint missing from its operation bindings: '+path)
    if covered!=set(registry):raise ValueError('Uncovered OpenAPI operations: '+', '.join(sorted(set(registry)-covered)))
    if websockets!=set(spec.get('x-websocket',{})):raise ValueError('Uncovered WebSocket contract')
    for file in (skill/'references').glob('*.md'):
        if file.name not in bindings['references'] and file.name!='endpoints.md' and ENDPOINT.search(file.read_text()):
            raise ValueError(file.name+': hosted API reference has no operation bindings')
    # Validate the entrypoint's HTTP examples too. Local helper commands are not
    # API request examples and are not parsed as curl.
    for match in FENCES.finditer((skill/'SKILL.md').read_text()):
        if match['language']=='bash' and not re.match(r'\s*curl\b',match['body']):continue
        if not match['annotation']:raise ValueError('SKILL.md: unbound API example')
        validate_example(spec,{'operations':list(registry)},match['operation'],match['media'],match['language'],match['body'])
        examples+=1
    return {'operations':len(covered),'references':len(bindings['references']),'examples':examples,'websockets':len(websockets)}


def check_live(spec, fetch=None):
    if fetch is None:
        def fetch():
            request=urllib.request.Request(SOURCE_URL,headers={'User-Agent':'Omneity-contract-check/1.0'})
            with urllib.request.urlopen(request,timeout=25) as response:
                if response.headers.get_content_type()!='application/json':raise ValueError('Live contract did not return JSON')
                return json.loads(response.read(2_000_001))
    if fetch()!=spec:raise ValueError('Live public contract differs from the pinned specification. Review before updating the skill.')


def main():
    from jsonschema import ValidationError
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-live',action='store_true',help='Also compare with the public portal; never changes the local contract')
    args=parser.parse_args();spec=json.loads((ROOT/'api/openapi.json').read_text())
    try:
        result=lint_skill(spec)
        if args.check_live:check_live(spec)
    except (ValueError,ValidationError) as exc:
        print(str(exc));return 1
    print('Skill contract checks passed: '+json.dumps(result))
    if args.check_live:print('Live public specification matches the pinned contract.')
    return 0


if __name__=='__main__':raise SystemExit(main())
