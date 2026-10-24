# Atlas Moroccan maps and routes

Read [the generated API contract](contracts/maps.md) for request fields, defaults, auth, and response types.

All routes use the normal Sawalni bearer key.

| Method and endpoint | Parameters |
|---|---|
| `GET /v1/atlas/search` | Required `q`; optional `model`, `channel`, `limit`, `place_type`, `name_filter`, `include_streets` |
| `GET /v1/atlas/osm/search` | Required `q`; optional `model`, `channel`, `limit` |
| `GET /v1/atlas/route` | Required `start_lat`, `start_lon`, `end_lat`, `end_lon` |
| `GET /v1/atlas/stats` | None |
| `GET /v1/atlas/models` | None |
| `GET /v1/atlas/health` | None |

Use `model: sawtone-v4`. Channels are `composite` (default), `phonetic`, `ortho`,
and `semantic`. Place search defaults to 50 results, range 1–200. Use 5–12 for an
interactive app. OSM search defaults to 8, range 1–20.
`place_type` accepts comma-separated locality types. `include_streets` defaults
to false. URL-encode queries. Preserve the user's original place spelling.

<!-- api-example: get_v1_atlas_search query -->
```bash
curl --get https://api.sawalni.com/v1/atlas/search \
  -H "Authorization: Bearer $SAWALNI_API_KEY" \
  --data-urlencode 'q=l3rayech' --data 'limit=5'
```

Search supports local spellings and cross-script variants. Routing returns
actual route geometry and instructions. Handle empty results and unavailable
routes. Do not invent fallback places or routes. Read `pricing.md` for the
current published pricing and request units.
