# Trail Usage

Use this when an existing trail probably covers the task.

Workflow:

```bash
herd trail search "target workflow"
herd trail run owner/name --action actionName --params '{"key":"value"}' --silent
```

CLI contract:

- Search before running unfamiliar trails.
- Prefer `--silent` for programmatic or LLM callers.
- Pass params as explicit JSON.
- Pin a version when the workflow must be repeatable.

App pattern:

- Run from a backend job or server route.
- Validate user-supplied params before invoking the CLI.
- Store trail, version, action, params hash, status, runtime, and result summary.
- Return normalized results to the frontend.

Failure handling:

- Trail not found: search broader terms or move to trail creation.
- Params rejected: inspect schema/examples and retry with corrected params.
- Site changed: move to trail creation/repair workflow.
