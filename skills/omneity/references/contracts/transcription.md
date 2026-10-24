# API contract: transcription

Generated from the pinned public OpenAPI file. Do not edit.

Source: [https://api.sawalni.com/openapi.json](https://api.sawalni.com/openapi.json).

Use the companion task reference for workflow guidance.

## post_v1_speech_transcribe

`POST /v1/speech/transcribe`

Transcribe uploaded audio

Authentication: `BearerAuth`.

Request content type: `multipart/form-data`.

| Field | Type | Required | Constraints and defaults |
|---|---|---|---|
| `audio` | string | yes |  |
| `model` | string | no | default="daktilo"; Discover supported public aliases with GET /v1/models. |
| `language` | string | no | Language hint. Confirm the supported codes for the selected public model. |

Success: `200`; content types: `application/json`.

## get_v1_models

`GET /v1/models`

List available model aliases

Authentication: `BearerAuth`.

Success: `200`; content types: `application/json`.

Model visibility does not guarantee entitlement or healthy capacity.

## WebSocket /v1/speech/transcribe/stream

This is a published OpenAPI extension, not an HTTP operation.

```json
{
  "url": "wss://api.sawalni.com/v1/speech/transcribe/stream",
  "protocol": "sawalni.transcribe.v1",
  "authentication": "Bearer header, x-api-key header, or sawalni-key.BASE64URL_KEY subprotocol from a browser. Do not put keys in query strings.",
  "start": {
    "type": "start",
    "model": "daktilo",
    "language": "ar",
    "sample_rate": 16000,
    "channels": 1,
    "audio_format": "pcm_s16le"
  },
  "client": "Send start JSON, binary PCM frames, then {type: stop}. Confirm selected model supports streaming; HTTP-only aliases can fail.",
  "server": [
    "ready",
    "partial",
    "sync",
    "final",
    "usage",
    "done",
    "error"
  ]
}
```
