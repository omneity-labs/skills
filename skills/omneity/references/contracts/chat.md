# API contract: chat

Generated from the pinned public OpenAPI file. Do not edit.

Source: [https://api.sawalni.com/openapi.json](https://api.sawalni.com/openapi.json).

Use the companion task reference for workflow guidance.

## post_v1_chat_completions

`POST /v1/chat/completions`

Generate a completion

Authentication: `BearerAuth`.

Request content type: `application/json`.

| Field | Type | Required | Constraints and defaults |
|---|---|---|---|
| `model` | string | yes |  |
| `messages` | object[] | yes | minItems=1 |
| `stream` | boolean | no | default=false |
| `temperature` | number | no | minimum=0; maximum=2 |
| `max_tokens` | integer | no | minimum=1 |
| `top_p` | number | no |  |
| `stop` | string or string[] | no |  |
| `tools` | object[] | no |  |
| `tool_choice` | string or object | no |  |
| `parallel_tool_calls` | boolean | no |  |
| `response_format` | object | no |  |
| `stream_options` | object | no |  |
| `modalities` | string[] | no |  |
| `audio` | object | no |  |

Example from the contract:

```json
{
  "model": "sawalni-beta",
  "messages": [
    {
      "role": "user",
      "content": "Explain this in Darija."
    }
  ]
}
```

Success: `200`; content types: `application/json`, `text/event-stream`.

OpenAI-compatible text and tool calls. Multimodal input/output depends on the model. Use Tarjamli's exact single-user translation template for tarjamli-v3.

## get_v1_models

`GET /v1/models`

List available model aliases

Authentication: `BearerAuth`.

Success: `200`; content types: `application/json`.

Model visibility does not guarantee entitlement or healthy capacity.
