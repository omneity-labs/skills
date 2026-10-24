# API contract: embeddings

Generated from the pinned public OpenAPI file. Do not edit.

Source: [https://api.sawalni.com/openapi.json](https://api.sawalni.com/openapi.json).

Use the companion task reference for workflow guidance.

## post_v1_embeddings

`POST /v1/embeddings`

embeddings

Authentication: `BearerAuth`.

Request content type: `application/json`.

| Field | Type | Required | Constraints and defaults |
|---|---|---|---|
| `model` | string | yes |  |
| `input` | string or string[] | yes |  |
| `encoding_format` | string | no | default="float"; Use float for portable TEI support. Other encodings depend on the deployment. |

Example from the contract:

```json
{
  "model": "madmon-beta",
  "input": [
    "A document"
  ]
}
```

Success: `200`; content types: `application/json`.

## get_v1_models

`GET /v1/models`

List available model aliases

Authentication: `BearerAuth`.

Success: `200`; content types: `application/json`.

Model visibility does not guarantee entitlement or healthy capacity.
