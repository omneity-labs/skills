# Omneity Skills

One Codex skill for building with the Omneity public ecosystem: sovereign
multilingual AI APIs, browser automation tools, and self-hosted search.

[Omneity Labs](https://www.omneitylabs.com/) builds production-grade language
models, language identification, embeddings, and agentic tools for languages and
workflows the mainstream AI stack often misses: Arabic dialects, Amazigh
languages, Moroccan Darija, African languages, cross-script text, browser-based
automation with your own infrastructure, and local/private hybrid search.

This repository packages that ecosystem as a single agent skill:

```text
omneity/
  SKILL.md
  references/
    functionality-guide.md
    chat.md
    embeddings.md
    language-id.md
    language-encoding.md
    rhyme-lyrics.md
    transcription.md
    text-alignment.md
    herd-trail-usage.md
    herd-trail-creation.md
    herd-browser-devices.md
    semango-setup-and-apps.md
    app-patterns.md
```

The goal is simple: when a user asks an AI coding agent to build something with
Omneity, the agent should discover the right capability, load the right
reference, and produce an application-quality integration without already
knowing the product names.

## Why One Skill

Most API skill repos are easy for humans to browse but hard for agents to
trigger. If the repo exposes one skill per model or endpoint, the agent first
has to know whether the user meant Sawalni, Madmon, Gherbal, Sawtone, Ziryab,
Daktilo, Sawalign, Herd, or Semango. That is backwards: users describe jobs,
not internal product taxonomy.

So this repo installs one broad skill, `omneity`, with a rich description and a
small router-style `SKILL.md`. Once the skill triggers, the agent loads focused
reference files only as needed.

That gives us both:

- Better discoverability: one obvious entrypoint for the whole public ecosystem.
- Better context hygiene: detailed docs stay in references and are loaded
  progressively.

## What You Can Build

Use this skill when building:

- Multilingual chat assistants for Darija, Amazigh, Arabic, French, English, and
  mixed-script users.
- RAG and semantic search apps over multilingual documents.
- Language, script, dialect, and Arabizi routing pipelines.
- Cross-script, fuzzy, phonetic, and typo-resistant search.
- Lyrics, rhyme, songwriting, and language-aware creative tools.
- Speech-to-text and voice-note ingestion flows.
- Subtitle, transcript, Premiere, and Final Cut alignment workflows.
- Browser automation products built on reusable Herd trails.
- Agent workflows that operate websites through your own browser sessions.
- Self-hosted search over files, docs, code, PDFs, and private knowledge bases.
- Combined research systems that collect pages, index artifacts, and synthesize
  answers with citations.

## Ecosystem

### Omneity Labs

[Omneity Labs](https://www.omneitylabs.com/) is a North-African and European AI
R&D lab building sovereign multilingual AI infrastructure. The public site
describes the mission as closing the language gap in AI with production-ready
LLMs, language ID, and embeddings for Arabic dialects, Amazigh, African
languages, and other underrepresented language communities.

Useful links:

- [Omneity Labs](https://www.omneitylabs.com/)
- [Projects](https://www.omneitylabs.com/projects)
- [Research](https://www.omneitylabs.com/research)
- [Hugging Face: omneity-labs](https://huggingface.co/omneity-labs)

### Sawalni API

[Sawalni API](https://api.sawalni.com/) is the hosted API surface for Omneity
models. It is designed to be OpenAI-compatible for common chat and embedding
workflows: change the base URL, use your Sawalni API key, and keep the rest of
your backend architecture familiar.

The API portal currently highlights:

- Sawalni: chat LLM for Moroccan Arabic, Amazigh, and multilingual workloads.
- Madmon: multilingual text embeddings for semantic search, clustering, and
  classification across Arabic varieties and underrepresented languages.
- Gherbal: language identification with script detection and batch processing.

Useful links:

- [Sawalni API Portal](https://api.sawalni.com/)
- [Sawalni Playground](https://sawalni.com/)
- [Sawalni model page](https://www.omneitylabs.com/models/sawalni)
- [Sawalni Python SDK](https://pypi.org/project/sawalni/)

### Sawalni

[Sawalni](https://www.omneitylabs.com/models/sawalni) is Omneity's multilingual
LLM for Moroccan and North African languages. It natively supports Moroccan
Arabic (Darija) in Arabic and Latin scripts, Hassaniya, Tachelhit, Tarifit, and
standardized Moroccan Tamazight in Tifinagh, while also supporting Arabic,
French, and English.

Use it for:

- Moroccan-language chatbots.
- Content generation in Darija, Amazigh, Arabic, French, and English.
- Cross-script understanding between Arabic script and Arabizi.
- Customer support, internal assistants, education tools, and culturally aware
  generation.

Reference in this skill: `references/chat.md`.

### Madmon

Madmon is Omneity's multilingual embeddings model for semantic representations
across Arabic dialects, Amazigh languages, and other underrepresented language
families. Use it for retrieval, classification, clustering, deduplication, and
RAG pipelines where generic English-first embeddings struggle.

Useful link:

- [Madmon research report](https://www.omneitylabs.com/research/madmon-multilingual-embeddings)

Reference in this skill: `references/embeddings.md`.

### Gherbal

Gherbal is Omneity's language identification capability. It is designed for
language, script, dialect, and Arabizi detection, including cases where common
language-ID libraries miss Arabic dialects or African languages.

Use it for:

- Routing user input to the right prompt, language, or model.
- Dataset filtering and multilingual analytics.
- Detecting script and language before indexing, generation, or UI selection.

Reference in this skill: `references/language-id.md`.

### Sawtone

Sawtone is the language and word encoding layer for phonetic, orthographic,
semantic, fuzzy, and cross-script retrieval. It is useful when users write the
same word across scripts, spellings, dialect conventions, or noisy user input.

Use it for:

- Cross-script name and word matching.
- Typo-resistant search.
- Arabizi and non-standardized spelling support.
- Retrieval keys that complement embeddings and lexical search.

Important: Sawtone is for language and word encoding. Sawalign is for text,
subtitle, and transcript alignment.

Reference in this skill: `references/language-encoding.md`.

### Ziryab

Ziryab is the rhyme and lyrics capability in the Omneity language stack. It is
for rhyme scoring, rhyme search, lyric structure analysis, and replacement
suggestions for songwriting tools.

Use it for:

- Rhyme candidate search.
- Rhyme quality scoring.
- Lyric replacement suggestions.
- Songwriting assistants for multilingual or dialectal contexts.

Reference in this skill: `references/rhyme-lyrics.md`.

### Daktilo

Daktilo covers speech-to-text workflows: uploaded audio, voice notes, video
audio tracks, transcript generation, and audio ingestion before downstream chat
or alignment.

Use it for:

- Voice-note transcription.
- Podcast or video transcript generation.
- Audio upload flows in web apps.
- Preparing transcripts for Sawalign.

Reference in this skill: `references/transcription.md`.

### Sawalign

Sawalign is Omneity's text alignment workflow for transcripts, subtitles, SRT,
VTT, Premiere XML, Final Cut XML, audio, and video timing. It belongs with the
Omneity API suite, but its job is media alignment rather than language encoding.

Use it for:

- Aligning a transcript to audio.
- Producing SRT or VTT subtitles.
- Repairing subtitle timing.
- Aligning editorial timelines for media production.

Reference in this skill: `references/text-alignment.md`.

### Herd

[Herd](https://herd.garden/) gives AI agents browser superpowers. It lets agents
run trails (ready-made automations), extract structured data, and operate websites through your own
browser sessions. Herd's public docs describe trails as pre-built automations
for specific websites and tasks, with support for browser extension setup,
registered browser devices, CLI usage, SDK usage, and MCP integration.

And the best part? You don't have to pay for any browser infrastructure, you can use your own, 
on your machine or remotely from your mobile and cloud agents.

This repo intentionally teaches Herd as CLI-first for agents: search for a
trail, run it with explicit JSON params, parse machine-readable output, and only
drop lower into SDK/MCP when the application needs it.

Useful links:

- [Herd](https://herd.garden/)
- [Herd getting started](https://herd.garden/docs/getting-started)
- [Trail Hub example: browser trail](https://herd.garden/trails/%40herd/browser)

References in this skill:

- `references/herd-trail-usage.md`
- `references/herd-trail-creation.md`
- `references/herd-browser-devices.md`

### Semango

Semango is the self-hosted search path in this skill. Use it when the task is to
run local/private hybrid search over files, docs, code, PDFs, tables, or a
knowledge base that should remain on your infrastructure.

Use it for:

- Local document search.
- Private RAG retrieval.
- Repository or folder indexing.
- Hybrid lexical and semantic search where you control deployment.

Reference in this skill: `references/semango-setup-and-apps.md`.

## How Agents Should Use This Repo

Agents should start with the installed `omneity` skill, then route by task:

| User says | Load |
|---|---|
| "Build a multilingual chat app" | `references/chat.md` |
| "Build RAG with hosted vectors" | `references/embeddings.md`, then `references/chat.md` |
| "Self-host search over our docs" | `references/semango-setup-and-apps.md` |
| "Detect language, dialect, or Arabizi" | `references/language-id.md` |
| "Match names across Arabic and Latin spelling" | `references/language-encoding.md` |
| "Find rhymes or improve lyrics" | `references/rhyme-lyrics.md` |
| "Transcribe audio" | `references/transcription.md` |
| "Make subtitles line up with audio" | `references/text-alignment.md` |
| "Call an existing browser automation" | `references/herd-trail-usage.md` |
| "Create or repair a trail" | `references/herd-trail-creation.md` |
| "Connect browser devices or consume events" | `references/herd-browser-devices.md` |
| "I do not know which capability I need" | `references/functionality-guide.md` |

For production application work, also load `references/app-patterns.md`.

## Installation

Install the `omneity` skill folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R skills/omneity ~/.codex/skills/
```

Then restart Codex so it picks up the new skill metadata.

If you are packaging this into another agent runtime, preserve the same
progressive structure: `SKILL.md` as the trigger and router, `references/` as
the detailed docs.

## Repository Layout

```text
.
├── README.md
├── FUNCTIONALITY_GUIDE.md
├── JTBD_ORGANIZATION.md
├── skills.json
├── evals/
│   ├── trigger_queries.json
│   └── app_build_queries.json
├── scripts/
│   ├── validate_skills.py
│   └── check_trigger_coverage.py
├── skills/
│   └── omneity/
│       ├── SKILL.md
│       └── references/
└── template/
    └── SKILL.md
```

## Evals

This repo treats discoverability as a first-class product surface.

The eval suite checks two layers:

1. Skill trigger coverage: should the single `omneity` skill load for this
   prompt?
2. Internal routing coverage: after the skill loads, which department/reference
   should the agent use?

Run:

```bash
python3 scripts/validate_skills.py
python3 scripts/check_trigger_coverage.py
```

Current eval fixtures live in:

- `evals/trigger_queries.json`
- `evals/app_build_queries.json`

The deterministic checker is a baseline. It is meant to catch obvious regressions
in descriptions and routing fixtures. For richer evaluation, pass model/router
predictions into:

```bash
python3 scripts/check_trigger_coverage.py --predictions predictions.json
```

Prediction shape:

```json
{
  "query-id": {
    "predicted_skills": ["omneity"],
    "predicted_departments": ["chat", "app-patterns"]
  }
}
```

## Design Principles

- One installed skill, many focused references.
- User intent first, product names second.
- Public docs only: no private inventories, unpublished endpoints, local paths,
  internal admin surfaces, service tokens, or plaintext secrets.
- Enough app-building detail to ship real integrations: backend boundaries,
  env vars, uploads, streaming, retries, caching, safe logging, failure states,
  and production readiness.
- CLI-first Herd guidance for agents, because it keeps setup lighter and reduces
  tool ambiguity.
- Self-hosting instructions for Semango, because deployment is part of the job.

## Useful Links

- [Omneity Labs](https://www.omneitylabs.com/)
- [Omneity Projects](https://www.omneitylabs.com/projects)
- [Sawalni API Portal](https://api.sawalni.com/)
- [Sawalni Playground](https://sawalni.com/)
- [Sawalni model page](https://www.omneitylabs.com/models/sawalni)
- [Sawalni Python SDK](https://pypi.org/project/sawalni/)
- [Madmon research report](https://www.omneitylabs.com/research/madmon-multilingual-embeddings)
- [Herd](https://herd.garden/)
- [Herd getting started](https://herd.garden/docs/getting-started)
- [Hugging Face: omneity-labs](https://huggingface.co/omneity-labs)

## API contract and current capabilities

The catalog also covers Tarjamli translation, Rescript script conversion, ASAT
speech, live Daktilo transcription, hosted
SawAlign jobs, Tarakib grammar, Maktaba web research, Akhbar news, Atlas maps,
Khizana collection search, and official widgets.

- [OpenAPI 3.1 contract](api/openapi.json)
- [Public pricing status](api/pricing.json)
- [Complete endpoint inventory](skills/omneity/references/endpoints.md)
- [Pricing and deployment caveats](skills/omneity/references/pricing.md)
- [Contract maintenance and skill binding checks](api/README.md)

Generate and validate the public artifacts:

```bash
python3 -m pip install -r scripts/requirements-api.txt
python3 scripts/generate_openapi.py
python3 scripts/generate_openapi.py --check
python3 scripts/lint_openapi.py
python3 scripts/validate_skills.py
python3 scripts/check_trigger_coverage.py
python3 -m unittest discover -s tests -v
```

The CI workflow runs these checks on pushes and pull requests. Source-aware
review also checks the API implementation in the maintainer environment.

The installed skill bundles a pinned OpenAPI snapshot. Each hosted API reference
links to generated request facts. All API JSON and curl examples are bound to
operation IDs and validated in CI. Use the installed `scripts/inspect_api.py`
helper to load a single operation instead of reading the entire contract.
