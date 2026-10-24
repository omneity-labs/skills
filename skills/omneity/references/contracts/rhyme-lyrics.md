# API contract: rhyme-lyrics

Generated from the pinned public OpenAPI file. Do not edit.

Source: [https://api.sawalni.com/openapi.json](https://api.sawalni.com/openapi.json).

Use the companion task reference for workflow guidance.

## post_v1_language_rhyme_score

`POST /v1/language/rhyme/score`

language rhyme score

Authentication: `BearerAuth`.

Request content type: `application/json`.

| Field | Type | Required | Constraints and defaults |
|---|---|---|---|
| `model` | string | no | default="sawtone-v4" |
| `language` | string | no |  |
| `script` | string | no |  |
| `pairs` | string[][] | yes | minItems=1 |
| `include_ipa` | boolean | no |  |
| `include_components` | boolean | no |  |

Example from the contract:

```json
{
  "pairs": [
    [
      "moon",
      "tune"
    ]
  ],
  "language": "eng_Latn"
}
```

Success: `200`; content types: `application/json`.

## post_v1_language_rhyme_search

`POST /v1/language/rhyme/search`

language rhyme search

Authentication: `BearerAuth`.

Request content type: `application/json`.

| Field | Type | Required | Constraints and defaults |
|---|---|---|---|
| `model` | string | no | default="sawtone-v4" |
| `language` | string | yes |  |
| `script` | string | no |  |
| `query` | string | yes | minLength=1 |
| `candidates` | string[] | no |  |
| `vocabulary` | string | no | default="common-lyrics"; enum=["raw", "common", "common-lyrics"] |
| `top_k` | integer | no | default=50 |
| `min_score` | number | no |  |
| `include_ipa` | boolean | no |  |

Example from the contract:

```json
{
  "query": "rain",
  "language": "eng_Latn",
  "top_k": 10
}
```

Success: `200`; content types: `application/json`.

## post_v1_language_lyrics_suggest-replacements

`POST /v1/language/lyrics/suggest-replacements`

language lyrics suggest-replacements

Authentication: `BearerAuth`.

Request content type: `application/json`.

| Field | Type | Required | Constraints and defaults |
|---|---|---|---|
| `model` | string | no | default="sawtone-v4" |
| `language` | string | yes |  |
| `script` | string | no |  |
| `line` | string | yes | minLength=1 |
| `target` | string | no |  |
| `vocabulary` | string | no | default="common-lyrics"; enum=["raw", "common", "common-lyrics"] |
| `top_k` | integer | no | default=20 |
| `weights` | object | no |  |
| `include_components` | boolean | no | default=true |

Example from the contract:

```json
{
  "line": "I keep my heart above the rain",
  "target": "rain",
  "language": "eng_Latn"
}
```

Success: `200`; content types: `application/json`.

## post_v1_language_lyrics_score

`POST /v1/language/lyrics/score`

language lyrics score

Authentication: `BearerAuth`.

Request content type: `application/json`.

| Field | Type | Required | Constraints and defaults |
|---|---|---|---|
| `model` | string | no | default="sawtone-v4" |
| `language` | string | yes |  |
| `script` | string | no |  |
| `text` | string | yes | minLength=1 |
| `rhyme_threshold` | number | no | default=0.64 |
| `include_internal_rhymes` | boolean | no | default=true |

Example from the contract:

```json
{
  "text": "I wait in rain\nI take the train",
  "language": "eng_Latn"
}
```

Success: `200`; content types: `application/json`.
