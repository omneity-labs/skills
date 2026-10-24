# Chat and multimodal generation

Read [the generated API contract](contracts/chat.md) for request fields, defaults, auth, and response types.

Use `POST /v1/chat/completions`. Use `sawalni-beta` for the main model.
Use `sawalni-mini-beta` for the small model.
Read `translation.md` before using `tarjamli-v3`.

<!-- api-example: post_v1_chat_completions application/json -->
```json
{"model":"sawalni-beta","messages":[{"role":"user","content":"Explain this in Darija."}],"max_tokens":512,"stream":true}
```

Supported request fields include `temperature`, `max_tokens`, `top_p`, `stop`,
`tools`, `tool_choice`, `parallel_tool_calls`, `response_format`, and
`stream_options`. Tool support and output quality depend on the model.
Validate function arguments before execution. Preserve tool call IDs in replies.
Parse structured output and validate it against the application's schema.

For streaming, parse SSE frames across network chunk boundaries. Read
`choices[].delta`. Stop at `[DONE]`. A disconnected stream can have incurred
usage. Do not repeat a tool action when retrying a completion.

## Images and audio

For image input, send message content parts with `type: "image_url"` and
`image_url: {"url": "data:image/jpeg;base64,..."}` or a supported image URL.
For recorded audio, use `type: "input_audio"` and
`input_audio: {"format": "wav", "data": "BASE64_AUDIO"}`.
Use a valid mono 16 kHz WAV for native voice input. Keep the original recording.
Multimodal support is model-specific. Do not assume that mini or translation
models support the same media as `sawalni-beta`.

For text and voice output, use `modalities: ["text", "audio"]`,
`audio: {"voice": "male-1", "format": "pcm16"}`, and `stream: true`.
Handle audio and text deltas separately. Use `speech-synthesis.md` for standalone
speech. Check the selected deployment's audio format support.

Keep API keys on the backend. Persist the final message after a successful
stream. Read `pricing.md` before estimating a text-and-audio workflow.
