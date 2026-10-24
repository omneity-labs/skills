# Tarakib grammar analysis

Read [the generated API contract](contracts/grammar.md) for request fields, defaults, auth, and response types.

Use `POST /v1/tarakib/analyze`.

<!-- api-example: post_v1_tarakib_analyze application/json -->
```json
{"text":"ذهب الطفل إلى المدرسة.","language":"ar","tasks":["pos","morphology","dependencies"],"morphology_threshold":0.5}
```

Provide exactly one of `text` or `tokens`. `text` has a 20,000-character limit.
`tokens` is an array of non-whitespace single tokens. A request can contain at
most 96 tokens. Split longer documents at sentence boundaries.

`language` is optional. Supported tasks are `pos`, `morphology`, and
`dependencies`. All tasks run by default. `morphology_threshold` defaults to
0.5 and ranges from 0.05 to 0.95.

Use `GET /v1/tarakib/models` and `GET /v1/tarakib/languages` for discovery.
Read token-level outputs for POS, morphology, and dependencies. Preserve token
boundaries when mapping results to the source. Do not treat model labels as
human-reviewed grammar annotations.

The default gateway rate is 60 requests per minute, burst 8, with two concurrent
analyses per key. Deployment settings can change these limits. Follow returned
rate and Retry-After headers. Read `pricing.md` before estimating costs.
