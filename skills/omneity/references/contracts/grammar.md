# API contract: grammar

Generated from the pinned public OpenAPI file. Do not edit.

Source: [https://api.sawalni.com/openapi.json](https://api.sawalni.com/openapi.json).

Use the companion task reference for workflow guidance.

## post_v1_tarakib_analyze

`POST /v1/tarakib/analyze`

tarakib analyze

Authentication: `BearerAuth`.

Request content type: `application/json`.

| Field | Type | Required | Constraints and defaults |
|---|---|---|---|
| `text` | string | no | maxLength=20000 |
| `tokens` | string[] | no | maxItems=96 |
| `language` | string | no |  |
| `tasks` | string[] | no |  |
| `morphology_threshold` | number | no | default=0.5; minimum=0.05; maximum=0.95 |

Request alternatives: `[{"required": ["text"], "not": {"required": ["tokens"]}}, {"required": ["tokens"], "not": {"required": ["text"]}}]`.

Example from the contract:

```json
{
  "text": "ذهب الطفل إلى المدرسة.",
  "language": "ar"
}
```

Success: `200`; content types: `application/json`.

## get_v1_tarakib_models

`GET /v1/tarakib/models`

tarakib models

Authentication: `BearerAuth`.

Success: `200`; content types: `application/json`.

## get_v1_tarakib_languages

`GET /v1/tarakib/languages`

tarakib languages

Authentication: `BearerAuth`.

Success: `200`; content types: `application/json`.
