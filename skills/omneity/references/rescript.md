# Rescript script conversion

Read [the generated API contract](contracts/rescript.md) for request fields, defaults, auth, and response types.

Use `POST /v1/language/transliterate`.
`POST /v1/language/rescript` is a compatibility alias.

<!-- api-example: post_v1_language_transliterate application/json -->
```json
{"model":"rescript-v1","input":"salam kif dayr","source_code":"ary_Latn","target_code":"ary_Arab","max_candidates":3,"min_overlap":0.9}
```

`input` is required. It accepts a string or string array.
The model defaults to `rescript-v1`. `target_code` defaults to `ary_Arab`.
Supply the target code explicitly. `source_code` is optional metadata.

Use `max_candidates: 3` for a portable request. Confirm current candidate
limits and pricing before requesting more candidates.

Other fields are `min_overlap` (default 0.90), `include_candidates` (false),
`max_decoder_len` (64; range 8–128), and `seed` (20260628).
The compatibility fields are `sample_candidates` and
`min_source_prediction_score`. Prefer the canonical names.

The service decodes words separately and preserves whitespace. Inspect
sentence and word acceptance before using the result. Return rejected or
uncertain output for review. This converts script; use Tarjamli to translate
meaning. Read `pricing.md` before estimating costs.
