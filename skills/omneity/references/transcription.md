# Daktilo transcription

Read [the generated API contract](contracts/transcription.md) for request fields, defaults, auth, and response types.

## Uploaded files

Use `POST /v1/speech/transcribe` with `multipart/form-data`.
The file field is `audio`. It is not the OpenAI `file` field.

<!-- api-example: post_v1_speech_transcribe multipart/form-data -->
```bash
curl https://api.sawalni.com/v1/speech/transcribe \
  -H "Authorization: Bearer $SAWALNI_API_KEY" \
  -F audio=@recording.wav -F model=daktilo -F language=ar
```

The gateway defaults to `daktilo` when the model is omitted. Discover aliases
with `GET /v1/models`. The public compatibility aliases include `daktilo-v1`
and `daktilo-v2`. Confirm language support for the selected model.

The response has `text`, `language`, `model`, `duration`, and `usage`.
Use word alignment when precise timestamps are required. The documented file
upload limit is 100 MB. Validate the accepted size before upload.

## Live speech

Connect to `wss://api.sawalni.com/v1/speech/transcribe/stream`.
Use a bearer header from a backend client. Browser clients can send
`sawalni.transcribe.v1` and `sawalni-key.BASE64URL_KEY` as WebSocket subprotocols.
Use an ephemeral or tightly scoped browser credential. Never put a key in a URL.

First send:

<!-- api-example: ws:/v1/speech/transcribe/stream start -->
```json
{"type":"start","model":"daktilo","language":"ar","sample_rate":16000,"channels":1,"audio_format":"pcm_s16le"}
```

Send binary frames containing mono PCM16 little-endian samples at 16 kHz.
Use `{"type":"flush"}` for a partial decode and `{"type":"stop"}` to finish.
Handle `ready`, `partial`, `sync`, `final`, `usage`, `done`, and `error` events.
Partial text can change. Preserve committed text and the final snapshot.
An HTTP transcription alias does not guarantee a streaming backend.
Use a known stream-capable alias; confirm streaming support before opening a session.

Read `chat.md` for native model audio attachments. Read `text-alignment.md` for
subtitles. Read `pricing.md` for separate file and streaming audio rates.
