# Trail Creation

Use this when no trail exists, an existing trail fails, or the task asks to
author, test, debug, package, or publish a browser automation trail.

Iteration loop:

1. Define the job, inputs, outputs, and success criteria.
2. Create a local trail with actions and typed params.
3. Use stable URL templates and selectors.
4. Run locally against a real fixture.
5. Capture logs, screenshots, and result artifacts.
6. Repair selectors/actions until the output is stable.
7. Package and publish or pin a private/local version.

Trail structure:

```text
trail/
  trail.json
  actions/
  fixtures/
  README.md
```

Best practices:

- Prefer semantic selectors, labels, and stable attributes over fragile CSS.
- Separate navigation, extraction, mutation, and verification actions.
- Make actions idempotent when possible.
- Include sample params and expected result shape.
- Treat login and secrets as runtime inputs, not committed files.
