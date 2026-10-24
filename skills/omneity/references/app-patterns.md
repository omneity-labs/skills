# App Patterns

## Backend Boundaries

Keep secrets server-side. Browser clients should call your backend, and your
backend should call hosted Omneity APIs, Herd CLI jobs, or Semango HTTP APIs.

Use env vars:

```text
SAWALNI_API_KEY=...
SAWALNI_BASE_URL=https://api.sawalni.com
HERD_API_KEY=...
SEMANGO_BASE_URL=http://localhost:8181
```

## Capability Composition

- RAG with hosted vectors: chunk documents, call embeddings, store vectors, then
  call chat with compact context.
- RAG with self-hosted search: index with Semango, retrieve source snippets,
  then call chat with citations.
- Audio subtitles: transcribe audio, then align transcript/subtitles with
  Sawalign.
- Website research: run Herd trail, save artifacts, index with Semango, then
  summarize with chat.

## Retries And Failure States

Follow `Retry-After` for `429` and transient capacity errors. Use bounded
backoff and explicit timeouts. A network failure can occur after a paid request
was accepted. Do not blindly repeat research, generation, or a tool action.
Resume polling with an existing job ID. Do not retry `400`, `401`, `402`, or
`403` unchanged. There is no universal idempotency-key guarantee.

Show specific states: validating, uploading, queued, running, streaming,
indexing, complete, retryable failure, and non-retryable failure.

Read `pricing.md` before quoting costs. Use a separate credential for collection
search. Use widget session tokens only with their intended collection or bot.
Do not assume that model discovery grants access to every model. Preserve
response content types: JSON, SSE, WAV, multipart uploads, and raw PCM differ.
Propagate cancellation when a client disconnects.

## Privacy And Logging

Log metadata by default: endpoint or command, model alias, trail action, status,
latency, request ID, token counts, byte counts, and params hash. Avoid raw user
content, audio, private documents, API keys, and full generated output unless
users opted into diagnostics.
