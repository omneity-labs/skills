# API contract: maps

Generated from the pinned public OpenAPI file. Do not edit.

Source: [https://api.sawalni.com/openapi.json](https://api.sawalni.com/openapi.json).

Use the companion task reference for workflow guidance.

## get_v1_atlas_search

`GET /v1/atlas/search`

Search Moroccan places

Authentication: `BearerAuth`.

| Parameter | Location | Type | Required | Constraints and defaults |
|---|---|---|---|---|
| `q` | query | string | yes |  |
| `model` | query | string | no | default="sawtone-v4" |
| `channel` | query | string | no | default="composite"; enum=["composite", "phonetic", "ortho", "semantic"] |
| `limit` | query | integer | no | default=50; minimum=1; maximum=200 |
| `place_type` | query | string | no |  |
| `name_filter` | query | string | no |  |
| `include_streets` | query | boolean | no | default=false |

Success: `200`; content types: `application/json`.

## get_v1_atlas_osm_search

`GET /v1/atlas/osm/search`

Search named OSM features

Authentication: `BearerAuth`.

| Parameter | Location | Type | Required | Constraints and defaults |
|---|---|---|---|---|
| `q` | query | string | yes |  |
| `model` | query | string | no | default="sawtone-v4" |
| `channel` | query | string | no | default="composite"; enum=["composite", "phonetic", "ortho", "semantic"] |
| `limit` | query | integer | no | default=8; minimum=1; maximum=20 |

Success: `200`; content types: `application/json`.

## get_v1_atlas_route

`GET /v1/atlas/route`

Get a driving route

Authentication: `BearerAuth`.

| Parameter | Location | Type | Required | Constraints and defaults |
|---|---|---|---|---|
| `start_lat` | query | number | yes |  |
| `start_lon` | query | number | yes |  |
| `end_lat` | query | number | yes |  |
| `end_lon` | query | number | yes |  |

Success: `200`; content types: `application/json`.

## get_v1_atlas_stats

`GET /v1/atlas/stats`

Read Atlas stats

Authentication: `BearerAuth`.

Success: `200`; content types: `application/json`.

## get_v1_atlas_models

`GET /v1/atlas/models`

Read Atlas models

Authentication: `BearerAuth`.

Success: `200`; content types: `application/json`.

## get_v1_atlas_health

`GET /v1/atlas/health`

Read Atlas health

Authentication: `BearerAuth`.

Success: `200`; content types: `application/json`.
