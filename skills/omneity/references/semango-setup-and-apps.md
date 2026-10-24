# Semango Setup And Apps

Use this when installing or building on self-hosted Semango.

## Setup

```bash
semango init
semango index
semango server
```

Docker:

```bash
docker run -p 8181:8181 -v "$(pwd):/workspace" ghcr.io/omarkamali/semango:latest
```

## Configuration

Tune `semango.yml` before indexing:

- Include only useful content roots.
- Exclude dependencies, build outputs, caches, generated files, media blobs, and
  secrets.
- Pick an embedding provider that matches your privacy/deployment constraints.
- Use persistent storage for indexes.

## App Pattern

Call `POST /api/v1/search` from the backend. Show indexing/freshness state in
the UI. For chat apps, retrieve results, show source snippets, then pass compact
context to Omneity chat.

## Production

Put Semango behind your own auth boundary. Monitor health, stats, index size,
query latency, and failed indexing jobs.
