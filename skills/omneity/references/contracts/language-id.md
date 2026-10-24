# API contract: language-id

Generated from the pinned public OpenAPI file. Do not edit.

Source: [https://api.sawalni.com/openapi.json](https://api.sawalni.com/openapi.json).

Use the companion task reference for workflow guidance.

## post_v1_language_identify

`POST /v1/language/identify`

language identify

Authentication: `BearerAuth`.

Request content type: `application/json`.

| Field | Type | Required | Constraints and defaults |
|---|---|---|---|
| `model` | string | yes |  |
| `input` | string or string[] | yes |  |
| `top` | integer | no | default=1; Positive k returns top-k predictions; non-positive values request all predictions. |

Example from the contract:

```json
{
  "model": "gherbal-v4",
  "input": "salam kif dayr?",
  "top": 3
}
```

Success: `200`; content types: `application/json`.
