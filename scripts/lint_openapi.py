#!/usr/bin/env python3
"""Validate OpenAPI, local references, examples, and skill endpoint references."""
import json
import re
from pathlib import Path
from jsonschema import Draft202012Validator
from openapi_spec_validator import validate

ROOT = Path(__file__).resolve().parents[1]


def lint(spec, references):
    validate(spec)
    ids = []
    for path, methods in spec["paths"].items():
        for method, operation in methods.items():
            ids.append(operation["operationId"])
            assert operation.get("summary"), (method, path, "missing summary")
            for value in operation.get("requestBody", {}).get("content", {}).values():
                if "example" in value:
                    schema = value["schema"]
                    if "$ref" in schema:
                        schema = spec["components"]["schemas"][schema["$ref"].split("/")[-1]]
                    Draft202012Validator(schema).validate(value["example"])
    assert len(ids) == len(set(ids)), "Duplicate operationId"
    for schema in spec["components"]["schemas"].values():
        Draft202012Validator.check_schema(schema)
    for file in references.glob("*.md"):
        for method, path in re.findall(r"\b(GET|POST|PUT|DELETE|PATCH) (/v1/[^\s`?,'\"]+|/api/public/[^\s`?,'\"]+)", file.read_text()):
            normalized = lambda p: re.sub(r"\{[^}]+\}", "{}", p)
            assert any(normalized(path) == normalized(p) and method.lower() in methods for p, methods in spec["paths"].items()), f"{file.name}: unknown endpoint {method} {path}"
    return len(ids)


if __name__ == "__main__":
    from skill_openapi import lint_skill
    spec = json.loads((ROOT / "api/openapi.json").read_text())
    count = lint(spec, ROOT / "skills/omneity/references")
    coverage = lint_skill(spec)
    print(f"OpenAPI, examples, and skill endpoints passed ({count} HTTP operations).")
    print("Skill contract coverage: " + json.dumps(coverage))
