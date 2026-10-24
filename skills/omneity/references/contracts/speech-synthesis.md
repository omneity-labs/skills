# API contract: speech-synthesis

Generated from the pinned public OpenAPI file. Do not edit.

Source: [https://api.sawalni.com/openapi.json](https://api.sawalni.com/openapi.json).

Use the companion task reference for workflow guidance.

## post_v1_audio_speech

`POST /v1/audio/speech`

Synthesize speech audio

Authentication: `BearerAuth`.

Request content type: `application/json`.

| Field | Type | Required | Constraints and defaults |
|---|---|---|---|
| `model` | string | no | default="asat" |
| `input` | string | yes | minLength=1 |
| `voice` | string | no | default="male-1" |
| `response_format` | string | no | default="wav"; wav is the portable choice. pcm16 support depends on the selected deployment. |
| `stream` | boolean | no | default=false |

Example from the contract:

```json
{
  "model": "asat",
  "input": "مرحبا بكم",
  "response_format": "wav"
}
```

Success: `200`; content types: `audio/wav`.

## post_v1_speech_synthesize

`POST /v1/speech/synthesize`

Synthesize speech audio

Authentication: `BearerAuth`.

Request content type: `application/json`.

| Field | Type | Required | Constraints and defaults |
|---|---|---|---|
| `model` | string | no | default="asat" |
| `input` | string | yes | minLength=1 |
| `voice` | string | no | default="male-1" |
| `response_format` | string | no | default="wav"; wav is the portable choice. pcm16 support depends on the selected deployment. |
| `stream` | boolean | no | default=false |

Example from the contract:

```json
{
  "model": "asat",
  "input": "مرحبا بكم",
  "response_format": "wav"
}
```

Success: `200`; content types: `audio/wav`.
