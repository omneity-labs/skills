# Language identification

Read [the generated API contract](contracts/language-id.md) for request fields, defaults, auth, and response types.

Use `POST /v1/language/identify`.

<!-- api-example: post_v1_language_identify application/json -->
```json
{"model":"gherbal-v4","input":["salam kif dayr?","Bonjour"],"top":3}
```

Both `model` and `input` are required. `input` is a string or string array.
`top` defaults to 1. A non-positive value requests all predictions in the current
handler. Prefer a small positive value for normal routing.

The response has `data[].input` and
`data[].predictions[].language` / `confidence`, plus `model` and `usage`.
Labels can encode language and script. Do not replace this shape with a single
`language` field. Keep low-confidence results visible to the caller.

Batch independent inputs. Use language ID when it changes routing or indexing.
Do not infer nationality from language. Read `pricing.md` before estimating costs.
