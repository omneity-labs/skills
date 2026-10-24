"""Reviewed public contract. Generate artifacts with generate_openapi.py.

Raw Request handlers do not expose complete FastAPI schemas. Keep these explicit
definitions under source review; the private source gate detects API changes.
"""
from __future__ import annotations

S = {"type": "string"}
N = {"type": "number"}
I = {"type": "integer"}
B = {"type": "boolean"}
FILE = {"type": "string", "format": "binary"}


def string(default=None, **kw):
    return {**S, **({"default": default} if default is not None else {}), **kw}


def array(items=S, **kw):
    return {"type": "array", "items": items, **kw}


def obj(properties=None, required=(), **kw):
    return {"type": "object", "properties": properties or {}, **({"required": list(required)} if required else {}), **kw}


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


TEXT_INPUT = {"oneOf": [S, array()]}
CHANNEL = string("composite", enum=["composite", "phonetic", "ortho", "semantic"])
MESSAGE = obj({"role": string(enum=["system", "developer", "user", "assistant", "tool"]),
               "content": {"oneOf": [S, array(obj()), {"type": "null"}]},
               "tool_calls": array(obj()), "tool_call_id": S}, ["role"])
CHAT = obj({"model": S, "messages": array(MESSAGE, minItems=1), "stream": {**B, "default": False},
            "temperature": {**N, "minimum": 0, "maximum": 2}, "max_tokens": {**I, "minimum": 1},
            "top_p": N, "stop": TEXT_INPUT, "tools": array(obj()),
            "tool_choice": {"oneOf": [S, obj()]}, "parallel_tool_calls": B,
            "response_format": obj({"type": S}), "stream_options": obj({"include_usage": B}),
            "modalities": array(string(enum=["text", "audio"])),
            "audio": obj({"voice": string("male-1"), "format": string("pcm16")})}, ["model", "messages"])

SCHEMAS = {
    "ChatRequest": CHAT,
    "ChatResponse": obj({"id": S, "object": S, "created": I, "model": S,
                         "choices": array(obj({"index": I, "message": MESSAGE, "finish_reason": {"type": ["string", "null"]}})),
                         "usage": obj()}, ["choices"]),
    "EmbeddingRequest": obj({"model": S, "input": TEXT_INPUT,
        "encoding_format": string("float", description="Use float for portable TEI support. Other encodings depend on the deployment.")}, ["model", "input"]),
    "EmbeddingResponse": obj({"object": S, "model": S, "data": array(obj({"index": I, "embedding": array(N)})), "usage": obj()}, ["data"]),
    "IdentifyRequest": obj({"model": string(examples=["gherbal-v4"]), "input": TEXT_INPUT, "top": {**I, "default": 1, "description": "Positive k returns top-k predictions; non-positive values request all predictions."}}, ["model", "input"]),
    "IdentifyResponse": obj({"model": S, "data": array(obj({"input": S, "predictions": array(obj({"language": S, "confidence": N}))})), "usage": obj()}, ["data"]),
    "EncodeRequest": obj({"model": string(examples=["sawtone-v4"]), "input": TEXT_INPUT, "channel": CHANNEL}, ["model", "input"]),
    "EncodeResponse": obj({"model": S, "data": array(obj({"input": S, "embedding": array(N)})), "channel": S, "dimensions": I, "usage": obj()}, ["data"]),
    "RescriptRequest": obj({"model": string("rescript-v1"), "input": TEXT_INPUT, "source_code": S,
                            "target_code": string("ary_Arab"), "max_candidates": {**I, "minimum": 1, "maximum": 32,
                                "description": "Use 1 to 3 candidates for a portable request. Confirm the current account limits."},
                            "min_overlap": {**N, "default": 0.9, "minimum": -1, "maximum": 1},
                            "max_decoder_len": {**I, "default": 64, "minimum": 8, "maximum": 128},
                            "seed": {**I, "default": 20260628}, "include_candidates": {**B, "default": False}}, ["input"]),
    "TarakibRequest": obj({"text": string(maxLength=20000), "tokens": array(string(pattern=r"^\S+$"), maxItems=96),
                           "language": S, "tasks": array(string(enum=["pos", "morphology", "dependencies"])),
                           "morphology_threshold": {**N, "minimum": 0.05, "maximum": 0.95, "default": 0.5}},
                          oneOf=[{"required": ["text"], "not": {"required": ["tokens"]}}, {"required": ["tokens"], "not": {"required": ["text"]}}]),
    "TranscribeRequest": obj({"audio": FILE, "model": string("daktilo", description="Discover supported public aliases with GET /v1/models."),
                              "language": string(description="Language hint. Confirm the supported codes for the selected public model.")}, ["audio"]),
    "TranscribeResponse": obj({"text": S, "language": S, "model": S, "duration": N, "segments": array(obj()), "warnings": array(), "usage": obj()}, ["text"]),
    "AlignmentRequest": obj({"audio": {**FILE, "description": "Audio or video, at most 128 MiB."}, "text": string(description="Transcript; at most 1,000,000 UTF-8 bytes.")}, ["audio", "text"]),
    "AlignmentJob": obj({"job_id": S, "status": S, "step": S, "progress": N, "words_so_far": array(obj()), "srt_url": S, "usage": obj()}, ["job_id", "status"]),
    "SpeechRequest": obj({"model": string("asat"), "input": string(minLength=1), "voice": string("male-1"),
                          "response_format": string("wav", description="wav is the portable choice. pcm16 support depends on the selected deployment."),
                          "stream": {**B, "default": False}}, ["input"]),
    "SearchRequest": obj({"query": string(minLength=1), "limit": {**I, "default": 10}, "cursor": {"type": ["string", "null"]},
                          "filters": obj({"domains": array(), "languages": array(), "source_types": array(), "published_from": S, "published_to": S}),
                          "include_content": B, "include_text": B}, ["query"]),
    "SocialRequest": obj({"query": string(minLength=1), "language": S, "platform": S, "limit": {**I, "default": 8}}, ["query"]),
    "ResearchRequest": obj({"task": string(minLength=1), "mode": string("deep")}, ["task"]),
    "NewsSearchRequest": obj({"query": string(minLength=1), "filters": obj({"languages": array(), "categories": array()}), "limit": {**I, "default": 10}}, ["query"]),
    "KnowledgeSearchRequest": obj({"query": string(minLength=1, maxLength=1000), "limit": {**I, "minimum": 1, "maximum": 10, "default": 5}}, ["query"]),
    "KnowledgeSearchResponse": obj({"query": S, "results": array(obj({"sourceId": S, "sourceName": S, "chunk": I, "text": S, "score": N}))}, ["results"]),
    "Error": obj({"detail": {}, "error": {}}, description="Errors can contain FastAPI detail or an error object. Inspect the HTTP status first."),
    "Object": obj(description="Pass-through response. Additional service fields can be present."),
}

RHYME_COMMON = {"model": string("sawtone-v4"), "language": S, "script": S}
SCHEMAS.update({
    "RhymeScoreRequest": obj({**RHYME_COMMON, "pairs": array(array(string(minLength=1), minItems=2, maxItems=2), minItems=1), "include_ipa": B, "include_components": B}, ["pairs"]),
    "RhymeSearchRequest": obj({**RHYME_COMMON, "query": string(minLength=1), "candidates": array(), "vocabulary": string("common-lyrics", enum=["raw", "common", "common-lyrics"]), "top_k": {**I, "default": 50}, "min_score": N, "include_ipa": B}, ["query", "language"]),
    "LyricReplaceRequest": obj({**RHYME_COMMON, "line": string(minLength=1), "target": S, "vocabulary": string("common-lyrics", enum=["raw", "common", "common-lyrics"]), "top_k": {**I, "default": 20}, "weights": obj(), "include_components": {**B, "default": True}}, ["line", "language"]),
    "LyricScoreRequest": obj({**RHYME_COMMON, "text": string(minLength=1), "rhyme_threshold": {**N, "default": 0.64}, "include_internal_rhymes": {**B, "default": True}}, ["text", "language"]),
})


def parameter(name, schema=S, location="query", required=False, description=""):
    return {"name": name, "in": location, "required": required or location == "path", "schema": schema,
            **({"description": description} if description else {})}


def build():
    paths = {}

    def add(method, path, summary, tag, request=None, response="Object", status="200", media="application/json", output="application/json", params=(), security=None, description="", example=None):
        op = {"operationId": method + "_" + path.strip("/").replace("/", "_").replace("{", "").replace("}", ""),
              "summary": summary, "tags": [tag], "responses": {status: {"description": summary,
                 **({"content": {output: {"schema": ref(response) if output == "application/json" else {"type": "string", **({"format": "binary"} if output.startswith("audio/") else {})}}}} if status != "204" else {})},
                 **{str(code): {"description": desc, "content": {"application/json": {"schema": ref("Error")}}}
                    for code, desc in [(400, "Invalid request"), (401, "Missing or invalid credential"), (402, "Insufficient credit or plan allowance"), (403, "Access denied"), (404, "Resource not found"), (413, "Request too large"), (422, "Input validation failed"), (429, "Rate or capacity limit"), (503, "Service unavailable"), (504, "Upstream timeout")]}}}
        if description:
            op["description"] = description
        parameters = list(params)
        import re
        for name in re.findall(r"\{([^}]+)\}", path):
            parameters.append(parameter(name, I if name in {"page_id", "sequence"} else S, "path"))
        if parameters:
            op["parameters"] = parameters
        if security is not None:
            op["security"] = security
        if request:
            op["requestBody"] = {"required": True, "content": {media: {"schema": ref(request), **({"example": example} if example is not None else {})}}}
        paths.setdefault(path, {})[method] = op
        return op

    add("get", "/v1/models", "List available model aliases", "Discovery", description="Model visibility does not guarantee entitlement or healthy capacity.")
    add("get", "/v1/billing/balance", "Read the current credit balance", "Billing")
    chat = add("post", "/v1/chat/completions", "Generate a completion", "Chat", "ChatRequest", "ChatResponse",
               description="OpenAI-compatible text and tool calls. Multimodal input/output depends on the model. Use Tarjamli's exact single-user translation template for tarjamli-v3.",
               example={"model": "sawalni-beta", "messages": [{"role": "user", "content": "Explain this in Darija."}]})
    chat["responses"]["200"]["content"]["text/event-stream"] = {"schema": S, "example": 'data: {"choices":[{"delta":{"content":"Hello"}}]}\n\ndata: [DONE]\n\n'}
    for route, req, resp, tag, example in [
        ("embeddings", "EmbeddingRequest", "EmbeddingResponse", "Embeddings", {"model": "madmon-beta", "input": ["A document"]}),
        ("language/identify", "IdentifyRequest", "IdentifyResponse", "Language", {"model": "gherbal-v4", "input": "salam kif dayr?", "top": 3}),
        ("language/encode", "EncodeRequest", "EncodeResponse", "Language", {"model": "sawtone-v4", "input": ["دار", "dar"], "channel": "composite"}),
        ("language/transliterate", "RescriptRequest", "Object", "Language", {"model": "rescript-v1", "input": "salam", "target_code": "ary_Arab", "max_candidates": 3}),
        ("language/rescript", "RescriptRequest", "Object", "Language", None),
        ("language/rhyme/score", "RhymeScoreRequest", "Object", "Lyrics", {"pairs": [["moon", "tune"]], "language": "eng_Latn"}),
        ("language/rhyme/search", "RhymeSearchRequest", "Object", "Lyrics", {"query": "rain", "language": "eng_Latn", "top_k": 10}),
        ("language/lyrics/suggest-replacements", "LyricReplaceRequest", "Object", "Lyrics", {"line": "I keep my heart above the rain", "target": "rain", "language": "eng_Latn"}),
        ("language/lyrics/score", "LyricScoreRequest", "Object", "Lyrics", {"text": "I wait in rain\nI take the train", "language": "eng_Latn"}),
        ("tarakib/analyze", "TarakibRequest", "Object", "Grammar", {"text": "ذهب الطفل إلى المدرسة.", "language": "ar"}),
        ("maktaba/search", "SearchRequest", "Object", "Search", {"query": "Morocco solar energy", "limit": 5}),
        ("maktaba/social/search", "SocialRequest", "Object", "Search", {"query": "solar energy", "limit": 5}),
        ("maktaba/research", "ResearchRequest", "Object", "Search", {"task": "Research Morocco solar energy with sources", "mode": "deep"}),
        ("akhbar/search", "NewsSearchRequest", "Object", "News", {"query": "الطاقة الشمسية", "limit": 10}),
    ]:
        add("post", "/v1/" + route, route.replace("/", " "), tag, req, resp, example=example)
    for route in ["tarakib/models", "tarakib/languages", "maktaba/status", "maktaba/pages/{page_id}", "akhbar/articles/{article_id}", "akhbar/status"]:
        add("get", "/v1/" + route, route.replace("/", " "), "Discovery")
    for route in ["edition", "headlines"]:
        add("get", "/v1/akhbar/" + route, "Read news " + route, "News", params=[parameter("category")])
    add("post", "/v1/speech/transcribe", "Transcribe uploaded audio", "Speech", "TranscribeRequest", "TranscribeResponse", media="multipart/form-data")
    add("post", "/v1/speech/align", "Submit a subtitle alignment job", "Speech", "AlignmentRequest", "AlignmentJob", status="202", media="multipart/form-data")
    add("get", "/v1/speech/align/job/{job_id}", "Poll alignment job", "Speech", response="AlignmentJob")
    add("get", "/v1/speech/align/job/{job_id}/srt", "Download aligned subtitles", "Speech", output="text/plain")
    add("post", "/v1/speech/word-align", "Align words synchronously", "Speech", "AlignmentRequest", media="multipart/form-data")
    for route in ["audio/speech", "speech/synthesize"]:
        add("post", "/v1/" + route, "Synthesize speech audio", "Speech", "SpeechRequest", output="audio/wav", example={"model": "asat", "input": "مرحبا بكم", "response_format": "wav"})
    search_params = [parameter("q", required=True), parameter("model", string("sawtone-v4")), parameter("channel", CHANNEL)]
    add("get", "/v1/atlas/search", "Search Moroccan places", "Maps", params=[*search_params,
        parameter("limit", {**I, "minimum": 1, "maximum": 200, "default": 50}), parameter("place_type"), parameter("name_filter"), parameter("include_streets", {**B, "default": False})])
    add("get", "/v1/atlas/osm/search", "Search named OSM features", "Maps", params=[*search_params, parameter("limit", {**I, "minimum": 1, "maximum": 20, "default": 8})])
    add("get", "/v1/atlas/route", "Get a driving route", "Maps", params=[parameter(k, N, required=True) for k in ["start_lat", "start_lon", "end_lat", "end_lon"]])
    for route in ["stats", "models", "health"]:
        add("get", "/v1/atlas/" + route, "Read Atlas " + route, "Maps")
    add("post", "/api/public/knowledge/{id}/search", "Search a Khizana collection", "Knowledge", "KnowledgeSearchRequest", "KnowledgeSearchResponse", security=[{"KnowledgeKey": []}],
        description="Use this collection's search key. A general model API key does not replace it. CORS requires an explicitly configured origin.", example={"query": "What is the return policy?", "limit": 5})
    return {"openapi": "3.1.0", "info": {"title": "Omneity Public API", "version": "2026-10-24",
        "description": "Reviewed public HTTP contract. Generated from maintained definitions; checked against API source. Pass-through object responses are intentionally open. Prices are deployment-dependent; see the pricing reference."},
        "servers": [{"url": "https://api.sawalni.com"}], "security": [{"BearerAuth": []}], "paths": paths,
        "components": {"schemas": SCHEMAS, "securitySchemes": {
            "BearerAuth": {"type": "http", "scheme": "bearer"}, "KnowledgeKey": {"type": "http", "scheme": "bearer", "description": "Collection search key"}}},
        "x-websocket": {"/v1/speech/transcribe/stream": {"url": "wss://api.sawalni.com/v1/speech/transcribe/stream", "protocol": "sawalni.transcribe.v1",
            "authentication": "Bearer header, x-api-key header, or sawalni-key.BASE64URL_KEY subprotocol from a browser. Do not put keys in query strings.",
            "start": {"type": "start", "model": "daktilo", "language": "ar", "sample_rate": 16000, "channels": 1, "audio_format": "pcm_s16le"},
            "client": "Send start JSON, binary PCM frames, then {type: stop}. Confirm selected model supports streaming; HTTP-only aliases can fail.",
            "server": ["ready", "partial", "sync", "final", "usage", "done", "error"]}}}
