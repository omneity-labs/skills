# SawAlign transcript and word alignment

Read [the generated API contract](contracts/text-alignment.md) for request fields, defaults, auth, and response types.

Use transcription first if no transcript exists. Alignment maps supplied text
to audio. It does not replace speech recognition.

## Hosted subtitle jobs

1. `POST /v1/speech/align` with multipart fields `audio` and `text`.
2. Read `job_id` from the HTTP 202 response.
3. Poll `GET /v1/speech/align/job/{job_id}` with a bounded interval and deadline.
4. When status is `done`, use `GET /v1/speech/align/job/{job_id}/srt`.

Audio can be audio or video, up to 128 MiB. Text can be plain transcript or SRT,
up to 1,000,000 UTF-8 bytes. SRT timestamps are removed before alignment.
Processing responses can contain `progress`, `step`, and `words_so_far`.
Handle failed jobs. Do not submit a second paid job merely because polling is
slow. Keep the job ID and original input files.

## Synchronous word times

Use `POST /v1/speech/word-align` with the same multipart fields.
Read `words` from the JSON response. This is the word-timing path.
Use a longer request timeout than a normal text request.

## Local editorial workflows

The separate Sawalign package supports local transcript and editorial XML
workflows. Check the installed CLI help before selecting flags. The hosted
contract above provides JSON and SRT routes. Do not invent hosted Premiere,
Final Cut, or VTT export routes from local CLI features.

Save aligned outputs as new files. Let users preview and correct them.
Read `pricing.md` for audio-duration pricing.
