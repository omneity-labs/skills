# Public API contract maintenance

`openapi.json` is the public OpenAPI 3.1 contract. It covers hosted HTTP routes.
Its `x-websocket` extension records the live speech protocol. Operational routes are outside this contract.

`pricing.json` records public pricing status. Unverified prices are withheld.
Read the skill's pricing reference before quoting costs.

## Required update rule

When the Omneity API changes, update this contract and the Omneity skill in the
same change. This includes routes, parameters, defaults, validation limits,
response formats, model aliases, authentication, billing units, and prices.

Many gateway handlers parse a raw request. Runtime FastAPI output does not
describe those bodies. `scripts/api_contract.py` holds the reviewed definitions.
The generator does not infer undocumented constraints or execute API services.
Open pass-through response objects are deliberate. Add exact response fields
when the service guarantees them.

## Generation and lint

From this repository root:

```bash
python3 -m pip install -r scripts/requirements-api.txt
python3 scripts/generate_openapi.py
python3 scripts/generate_openapi.py --check
python3 scripts/lint_openapi.py
python3 scripts/validate_skills.py
python3 scripts/check_trigger_coverage.py
python3 -m unittest discover -s tests -v
```

The generator also writes the endpoint inventory, pricing status, installed
skill snapshot, hash lock, and focused contract references.
The CI workflow rejects stale generated files, invalid OpenAPI, invalid request
examples, unknown skill endpoints, and contract regression failures.

The source-aware maintainer gate compares the actual route inventory with this
contract. It also checks reviewed source fingerprints. Source changes require
review even when the path stays the same. Parameter and price changes can occur
without a new route.

Public CI can validate only this repository. The API project must also run the
source-aware gate before release. A green public CI run alone does not prove
parity with a running deployment.

## Public boundary

Include documented developer endpoints and public model aliases only. Exclude
application implementation routes, deployment topology, billing implementation
details, and unverified prices. Keep source audit findings in maintainer notes.

These artifacts do not deploy a new API schema endpoint or change service behavior.

## Skill binding checks

`skills/omneity/references/api-bindings.json` maps task references to OpenAPI
operation IDs. All 39 HTTP operations and the WebSocket extension must have a
binding. Generate contract facts from the spec. Keep workflow advice in the
hand-written task references.

Every JSON and curl example in a bound task reference needs a marker:

```text
<!-- api-example: post_v1_language_identify application/json -->
```

The marker belongs immediately before its code fence. The linter validates JSON
syntax, required fields, types, enums, numeric limits, and declared field names.
For curl, it also checks the HTTP method, URL, query parameters, and multipart
field names. It parses curl as data; it never executes examples or calls models.
The WebSocket start example is checked against the published extension.

Run `python3 scripts/skill_openapi.py` for the installed-skill checks. Public CI
also runs these checks through the OpenAPI linter. A missing operation binding,
unbound example, invalid request, stale generated table, stale bundled snapshot,
or changed snapshot hash fails validation.

Use `python3 scripts/skill_openapi.py --check-live` to compare the pinned file
with the public portal. This optional network check fails on drift. It does not
automatically import a changed contract. Review API changes before regeneration.
The normal checks run offline and are reproducible.

Installation must copy the entire `skills/omneity` folder. It includes the pinned
contract and `scripts/inspect_api.py`. The helper can list or inspect operations
without dependencies or network access. The test suite verifies this in an
isolated installation.

These checks do not verify API implementation behavior, translation quality,
pricing claims, or prose meaning. The source-aware gate and public release
review still apply. A permissive schema also limits what can be validated.
