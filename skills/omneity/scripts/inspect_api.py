#!/usr/bin/env python3
"""Show one operation from the installed skill's pinned public API contract."""
import argparse
import hashlib
import json
from pathlib import Path

SKILL=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation',nargs='?',help='OpenAPI operationId')
    parser.add_argument('--list',action='store_true',help='List operation IDs, methods, and paths')
    args=parser.parse_args()
    raw=(SKILL/'references/openapi.json').read_bytes()
    lock=json.loads((SKILL/'references/openapi-lock.json').read_text())
    if hashlib.sha256(raw).hexdigest()!=lock['sha256']:
        parser.error('The bundled API contract does not match its lock. Reinstall a validated skill.')
    spec=json.loads(raw); registry={op['operationId']:(method,path,op) for path,methods in spec['paths'].items() for method,op in methods.items()}
    if args.list:
        for name,(method,path,op) in registry.items():print(name+'  '+method.upper()+' '+path)
        return 0
    if args.operation not in registry:parser.error('Choose a valid operationId. Use --list to see the available operations.')
    method,path,op=registry[args.operation]
    schemas={}
    def collect(value):
        if isinstance(value,dict):
            reference=value.get('$ref','')
            if reference.startswith('#/components/schemas/'):
                name=reference.split('/')[-1]
                if name not in schemas:
                    schemas[name]=spec['components']['schemas'][name]
                    collect(schemas[name])
            for item in value.values():collect(item)
        elif isinstance(value,list):
            for item in value:collect(item)
    collect(op)
    security=op.get('security',spec.get('security',[]))
    schemes={name:spec['components']['securitySchemes'][name] for option in security for name in option}
    print(json.dumps({'source_url':lock['source_url'],'contract_sha256':lock['sha256'],
        'method':method.upper(),'path':path,'security':security,'operation':op,
        'components':{'schemas':schemas,'securitySchemes':schemes}},ensure_ascii=False,indent=2))
    return 0


if __name__=='__main__':raise SystemExit(main())
