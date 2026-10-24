# Ziryab rhymes and lyrics

Read [the generated API contract](contracts/rhyme-lyrics.md) for request fields, defaults, auth, and response types.

Use the following JSON endpoints. `model` defaults to `sawtone-v4`.

| Endpoint | Required body | Optional fields |
|---|---|---|
| `POST /v1/language/rhyme/score` | `pairs` | `language`, `script`, `include_ipa`, `include_components` |
| `POST /v1/language/rhyme/search` | `query`, `language` | `script`, `candidates`, `vocabulary`, `top_k`, `min_score`, `include_ipa` |
| `POST /v1/language/lyrics/suggest-replacements` | `line`, `language` | `target`, `script`, `vocabulary`, `top_k`, `weights`, `include_components` |
| `POST /v1/language/lyrics/score` | `text`, `language` | `script`, `rhyme_threshold`, `include_internal_rhymes` |

<!-- api-example: post_v1_language_rhyme_score application/json -->
```json
{"pairs":[["moon","tune"],["rain","train"]],"language":"eng_Latn","include_components":true}
```

Each pair contains exactly two non-empty words. The old `word_a` / `word_b`
request is invalid. Batch independent pairs in `pairs`.

<!-- api-example: post_v1_language_rhyme_search application/json -->
```json
{"query":"rain","language":"eng_Latn","vocabulary":"common-lyrics","top_k":10}
```

Search requires an available vocabulary for the language. Handle
`unsupported_language` and its `supported_languages` list. Do not assume that
all encoding languages have a rhyme index. The vocabulary default is
`common-lyrics`. Supported tiers are `raw`, `common`, and `common-lyrics`.

Rhyme scores are returned in `results[].rhyme_score`. Replacement suggestions
use `line` and optionally `target`. Lyric scoring takes one text string with
line breaks; it does not take a `lines` array. It defaults to
`rhyme_threshold: 0.64` and `include_internal_rhymes: true`.

Keep suggestions editable. Preserve the user's lyrics until they accept an
edit. Cache repeated searches. Read `pricing.md`: each scored pair is one
operation; each search, suggestion, or lyric-score request is one operation.
