# API contract: language-encoding

Generated from the pinned public OpenAPI file. Do not edit.

Source: [https://api.sawalni.com/openapi.json](https://api.sawalni.com/openapi.json).

Use the companion task reference for workflow guidance.

## post_v1_language_encode

`POST /v1/language/encode`

language encode

Authentication: `BearerAuth`.

Request content type: `application/json`.

| Field | Type | Required | Constraints and defaults |
|---|---|---|---|
| `model` | string | yes |  |
| `input` | string or string[] | yes |  |
| `channel` | string | no | default="composite"; enum=["composite", "phonetic", "ortho", "semantic"] |

Example from the contract:

```json
{
  "model": "sawtone-v4",
  "input": [
    "دار",
    "dar"
  ],
  "channel": "composite"
}
```

Success: `200`; content types: `application/json`.
