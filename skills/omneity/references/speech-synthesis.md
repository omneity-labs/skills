# ASAT speech synthesis

Read [the generated API contract](contracts/speech-synthesis.md) for request fields, defaults, auth, and response types.

Use `POST /v1/audio/speech`. `POST /v1/speech/synthesize` is an alias.

<!-- api-example: post_v1_audio_speech application/json -->
```json
{"model":"asat","input":"مرحبا بكم","voice":"male-1","response_format":"wav","stream":false}
```

`input` is required. Defaults are `model: "asat"`, `voice: "male-1"`,
`response_format: "wav"`, and `stream: false`.
Voice availability depends on the deployment. Use current documented voice IDs.
Do not send NFE, speed, CFG, or chunk-size fields. They are not public controls.

The response contains audio bytes. Do not parse it as JSON on success.
Check the content type before playback. JSON error bodies can still occur.
Use WAV for portable standalone requests. Confirm supported output formats
before selecting PCM.
For supported raw PCM output, confirm the sample rate and channel count.

`stream: true` changes delivery. It does not select a separate quality mode.
A streaming WAV can have placeholder RIFF lengths. Repair the RIFF and data
lengths after completion before saving it as a standalone file.

Read `pricing.md` before estimating generated audio costs.
