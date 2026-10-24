# Hosted API endpoints

Generated from the reviewed OpenAPI definitions. Do not edit this list.

Read `api/openapi.json` at the repository root for schemas and examples.

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/public/knowledge/{id}/search` | Search a Khizana collection |
| GET | `/v1/akhbar/articles/{article_id}` | akhbar articles {article_id} |
| GET | `/v1/akhbar/edition` | Read news edition |
| GET | `/v1/akhbar/headlines` | Read news headlines |
| POST | `/v1/akhbar/search` | akhbar search |
| GET | `/v1/akhbar/status` | akhbar status |
| GET | `/v1/atlas/health` | Read Atlas health |
| GET | `/v1/atlas/models` | Read Atlas models |
| GET | `/v1/atlas/osm/search` | Search named OSM features |
| GET | `/v1/atlas/route` | Get a driving route |
| GET | `/v1/atlas/search` | Search Moroccan places |
| GET | `/v1/atlas/stats` | Read Atlas stats |
| POST | `/v1/audio/speech` | Synthesize speech audio |
| GET | `/v1/billing/balance` | Read the current credit balance |
| POST | `/v1/chat/completions` | Generate a completion |
| POST | `/v1/embeddings` | embeddings |
| POST | `/v1/language/encode` | language encode |
| POST | `/v1/language/identify` | language identify |
| POST | `/v1/language/lyrics/score` | language lyrics score |
| POST | `/v1/language/lyrics/suggest-replacements` | language lyrics suggest-replacements |
| POST | `/v1/language/rescript` | language rescript |
| POST | `/v1/language/rhyme/score` | language rhyme score |
| POST | `/v1/language/rhyme/search` | language rhyme search |
| POST | `/v1/language/transliterate` | language transliterate |
| GET | `/v1/maktaba/pages/{page_id}` | maktaba pages {page_id} |
| POST | `/v1/maktaba/research` | maktaba research |
| POST | `/v1/maktaba/search` | maktaba search |
| POST | `/v1/maktaba/social/search` | maktaba social search |
| GET | `/v1/maktaba/status` | maktaba status |
| GET | `/v1/models` | List available model aliases |
| POST | `/v1/speech/align` | Submit a subtitle alignment job |
| GET | `/v1/speech/align/job/{job_id}` | Poll alignment job |
| GET | `/v1/speech/align/job/{job_id}/srt` | Download aligned subtitles |
| POST | `/v1/speech/synthesize` | Synthesize speech audio |
| POST | `/v1/speech/transcribe` | Transcribe uploaded audio |
| POST | `/v1/speech/word-align` | Align words synchronously |
| POST | `/v1/tarakib/analyze` | tarakib analyze |
| GET | `/v1/tarakib/languages` | tarakib languages |
| GET | `/v1/tarakib/models` | tarakib models |

WebSocket: `wss://api.sawalni.com/v1/speech/transcribe/stream`.
Read `transcription.md` for the session protocol.
