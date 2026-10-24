# API contract: knowledge-search

Generated from the pinned public OpenAPI file. Do not edit.

Source: [https://api.sawalni.com/openapi.json](https://api.sawalni.com/openapi.json).

Use the companion task reference for workflow guidance.

## post_v1_maktaba_search

`POST /v1/maktaba/search`

maktaba search

Authentication: `BearerAuth`.

Request content type: `application/json`.

| Field | Type | Required | Constraints and defaults |
|---|---|---|---|
| `query` | string | yes | minLength=1 |
| `limit` | integer | no | default=10 |
| `cursor` | string or null | no |  |
| `filters` | object | no |  |
| `include_content` | boolean | no |  |
| `include_text` | boolean | no |  |

Example from the contract:

```json
{
  "query": "Morocco solar energy",
  "limit": 5
}
```

Success: `200`; content types: `application/json`.

## post_v1_maktaba_social_search

`POST /v1/maktaba/social/search`

maktaba social search

Authentication: `BearerAuth`.

Request content type: `application/json`.

| Field | Type | Required | Constraints and defaults |
|---|---|---|---|
| `query` | string | yes | minLength=1 |
| `language` | string | no |  |
| `platform` | string | no |  |
| `limit` | integer | no | default=8 |

Example from the contract:

```json
{
  "query": "solar energy",
  "limit": 5
}
```

Success: `200`; content types: `application/json`.

## post_v1_maktaba_research

`POST /v1/maktaba/research`

maktaba research

Authentication: `BearerAuth`.

Request content type: `application/json`.

| Field | Type | Required | Constraints and defaults |
|---|---|---|---|
| `task` | string | yes | minLength=1 |
| `mode` | string | no | default="deep" |

Example from the contract:

```json
{
  "task": "Research Morocco solar energy with sources",
  "mode": "deep"
}
```

Success: `200`; content types: `application/json`.

## post_v1_akhbar_search

`POST /v1/akhbar/search`

akhbar search

Authentication: `BearerAuth`.

Request content type: `application/json`.

| Field | Type | Required | Constraints and defaults |
|---|---|---|---|
| `query` | string | yes | minLength=1 |
| `filters` | object | no |  |
| `limit` | integer | no | default=10 |

Example from the contract:

```json
{
  "query": "الطاقة الشمسية",
  "limit": 10
}
```

Success: `200`; content types: `application/json`.

## get_v1_maktaba_status

`GET /v1/maktaba/status`

maktaba status

Authentication: `BearerAuth`.

Success: `200`; content types: `application/json`.

## get_v1_maktaba_pages_page_id

`GET /v1/maktaba/pages/{page_id}`

maktaba pages {page_id}

Authentication: `BearerAuth`.

| Parameter | Location | Type | Required | Constraints and defaults |
|---|---|---|---|---|
| `page_id` | path | integer | yes |  |

Success: `200`; content types: `application/json`.

## get_v1_akhbar_articles_article_id

`GET /v1/akhbar/articles/{article_id}`

akhbar articles {article_id}

Authentication: `BearerAuth`.

| Parameter | Location | Type | Required | Constraints and defaults |
|---|---|---|---|---|
| `article_id` | path | string | yes |  |

Success: `200`; content types: `application/json`.

## get_v1_akhbar_status

`GET /v1/akhbar/status`

akhbar status

Authentication: `BearerAuth`.

Success: `200`; content types: `application/json`.

## get_v1_akhbar_edition

`GET /v1/akhbar/edition`

Read news edition

Authentication: `BearerAuth`.

| Parameter | Location | Type | Required | Constraints and defaults |
|---|---|---|---|---|
| `category` | query | string | no |  |

Success: `200`; content types: `application/json`.

## get_v1_akhbar_headlines

`GET /v1/akhbar/headlines`

Read news headlines

Authentication: `BearerAuth`.

| Parameter | Location | Type | Required | Constraints and defaults |
|---|---|---|---|---|
| `category` | query | string | no |  |

Success: `200`; content types: `application/json`.

## post_api_public_knowledge_id_search

`POST /api/public/knowledge/{id}/search`

Search a Khizana collection

Authentication: `KnowledgeKey`.

Request content type: `application/json`.

| Field | Type | Required | Constraints and defaults |
|---|---|---|---|
| `query` | string | yes | minLength=1; maxLength=1000 |
| `limit` | integer | no | default=5; minimum=1; maximum=10 |

Example from the contract:

```json
{
  "query": "What is the return policy?",
  "limit": 5
}
```

| Parameter | Location | Type | Required | Constraints and defaults |
|---|---|---|---|---|
| `id` | path | string | yes |  |

Success: `200`; content types: `application/json`.

Use this collection's search key. A general model API key does not replace it. CORS requires an explicitly configured origin.
