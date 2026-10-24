# API contract: rescript

Generated from the pinned public OpenAPI file. Do not edit.

Source: [https://api.sawalni.com/openapi.json](https://api.sawalni.com/openapi.json).

Use the companion task reference for workflow guidance.

## post_v1_language_transliterate

`POST /v1/language/transliterate`

language transliterate

Authentication: `BearerAuth`.

Request content type: `application/json`.

| Field | Type | Required | Constraints and defaults |
|---|---|---|---|
| `model` | string | no | default="rescript-v1" |
| `input` | string or string[] | yes |  |
| `source_code` | string | no |  |
| `target_code` | string | no | default="ary_Arab" |
| `max_candidates` | integer | no | minimum=1; maximum=32; Use 1 to 3 candidates for a portable request. Confirm the current account limits. |
| `min_overlap` | number | no | default=0.9; minimum=-1; maximum=1 |
| `max_decoder_len` | integer | no | default=64; minimum=8; maximum=128 |
| `seed` | integer | no | default=20260628 |
| `include_candidates` | boolean | no | default=false |

Example from the contract:

```json
{
  "model": "rescript-v1",
  "input": "salam",
  "target_code": "ary_Arab",
  "max_candidates": 3
}
```

Success: `200`; content types: `application/json`.

## post_v1_language_rescript

`POST /v1/language/rescript`

language rescript

Authentication: `BearerAuth`.

Request content type: `application/json`.

| Field | Type | Required | Constraints and defaults |
|---|---|---|---|
| `model` | string | no | default="rescript-v1" |
| `input` | string or string[] | yes |  |
| `source_code` | string | no |  |
| `target_code` | string | no | default="ary_Arab" |
| `max_candidates` | integer | no | minimum=1; maximum=32; Use 1 to 3 candidates for a portable request. Confirm the current account limits. |
| `min_overlap` | number | no | default=0.9; minimum=-1; maximum=1 |
| `max_decoder_len` | integer | no | default=64; minimum=8; maximum=128 |
| `seed` | integer | no | default=20260628 |
| `include_candidates` | boolean | no | default=false |

Success: `200`; content types: `application/json`.
