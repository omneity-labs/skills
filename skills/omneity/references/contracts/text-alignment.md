# API contract: text-alignment

Generated from the pinned public OpenAPI file. Do not edit.

Source: [https://api.sawalni.com/openapi.json](https://api.sawalni.com/openapi.json).

Use the companion task reference for workflow guidance.

## post_v1_speech_align

`POST /v1/speech/align`

Submit a subtitle alignment job

Authentication: `BearerAuth`.

Request content type: `multipart/form-data`.

| Field | Type | Required | Constraints and defaults |
|---|---|---|---|
| `audio` | string | yes | Audio or video, at most 128 MiB. |
| `text` | string | yes | Transcript; at most 1,000,000 UTF-8 bytes. |

Success: `202`; content types: `application/json`.

## get_v1_speech_align_job_job_id

`GET /v1/speech/align/job/{job_id}`

Poll alignment job

Authentication: `BearerAuth`.

| Parameter | Location | Type | Required | Constraints and defaults |
|---|---|---|---|---|
| `job_id` | path | string | yes |  |

Success: `200`; content types: `application/json`.

## get_v1_speech_align_job_job_id_srt

`GET /v1/speech/align/job/{job_id}/srt`

Download aligned subtitles

Authentication: `BearerAuth`.

| Parameter | Location | Type | Required | Constraints and defaults |
|---|---|---|---|---|
| `job_id` | path | string | yes |  |

Success: `200`; content types: `text/plain`.

## post_v1_speech_word-align

`POST /v1/speech/word-align`

Align words synchronously

Authentication: `BearerAuth`.

Request content type: `multipart/form-data`.

| Field | Type | Required | Constraints and defaults |
|---|---|---|---|
| `audio` | string | yes | Audio or video, at most 128 MiB. |
| `text` | string | yes | Transcript; at most 1,000,000 UTF-8 bytes. |

Success: `200`; content types: `application/json`.
