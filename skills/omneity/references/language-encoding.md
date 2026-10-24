# Sawtone word encoding

Read [the generated API contract](contracts/language-encoding.md) for request fields, defaults, auth, and response types.

Use `POST /v1/language/encode` for phonetic, orthographic, semantic, and
cross-script word representations.

<!-- api-example: post_v1_language_encode application/json -->
```json
{"model":"sawtone-v4","input":["دار","dar"],"channel":"composite"}
```

`model` and `input` are required. `input` accepts one string or a string array.
`channel` accepts `composite` (default), `phonetic`, `ortho`, or `semantic`.
The response has `data[].input`, `data[].embedding`, `channel`, `dimensions`,
`model`, and `usage`. This returns numerical vectors, not a textual encoding.
Read `dimensions` from the response. Keep the channel fixed within an index.

The service splits each input on whitespace. It pools word vectors for that
input. Batch independent strings in one request. Preserve original text for
display. Test retrieval with local spellings, Arabizi, and cross-script pairs.
Use `rescript.md` when the user needs converted text.

Read `pricing.md` before estimating costs.
