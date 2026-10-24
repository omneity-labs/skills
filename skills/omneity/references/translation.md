# Tarjamli translation

Read [the generated API contract](contracts/translation.md) for request fields, defaults, auth, and response types.

Call `POST /v1/chat/completions` with `model: "tarjamli-v3"`.
Translate Moroccan Arabic in Arabic or Latin script to exactly one of
`English`, `French`, or `Modern Standard Arabic`.

Use one user message with this exact content template:

```text
Translate this Moroccan Arabic text to TARGET. Return only the translation.

SOURCE_TEXT
```

Replace `TARGET` with one supported target name. Replace `SOURCE_TEXT` with the
source text. Do not add a system message, history, labels, or extra instructions.
Use `temperature: 0`. The 8,192-token context includes both input and output.

<!-- api-example: post_v1_chat_completions application/json -->
```json
{"model":"tarjamli-v3","messages":[{"role":"user","content":"Translate this Moroccan Arabic text to English. Return only the translation.\n\nسلام كيف داير؟"}],"temperature":0,"max_tokens":256}
```

Read `choices[0].message.content`. It contains the raw translation.
Use separate requests for separate targets. Preserve the template when using
this model. Read `pricing.md` before estimating translation cost.
