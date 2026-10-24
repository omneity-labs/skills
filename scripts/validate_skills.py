#!/usr/bin/env python3
"""Validate the public Omneity skills repo."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
REGISTRY = ROOT / "skills.json"
EVALS_DIR = ROOT / "evals"

REQUIRED_SECTIONS = [
    "## Quick start",
    "## API contract",
    "## Build apps with this",
    "## Best practices",
    "## Related skills",
]

LOCAL_PATH_PATTERN = "|".join([r"/Use" + "rs/", r"~/Co" + "de", r"/Vol" + "umes/", r"/da" + "ta/"])

FORBIDDEN_PATTERNS = {
    "local_path": re.compile(LOCAL_PATH_PATTERN, re.I),
    "secret_literal": re.compile(
        r"(sk-[A-Za-z0-9_-]{20,}|xox[baprs]-[A-Za-z0-9-]{20,}|SECRET\s*=\s*['\"][^'\"]+)",
        re.I,
    ),
}


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    body = text[4:end]
    data: dict[str, str] = {}
    for line in body.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
    return data


def check_file(path: Path, known_slugs: set[str]) -> list[str]:
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8", errors="replace")
    errors: list[str] = []

    meta = parse_frontmatter(text)
    if not meta.get("name"):
        errors.append(f"{rel}: missing frontmatter name")
    if not meta.get("description") or len(meta["description"].split()) < 6:
        errors.append(f"{rel}: missing or too-short frontmatter description")

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"{rel}: missing required section {section}")

    for label, pattern in FORBIDDEN_PATTERNS.items():
        for match in pattern.finditer(text):
            errors.append(f"{rel}: forbidden {label} at line {text.count(chr(10), 0, match.start()) + 1}")

    related_match = re.search(r"## Related skills\s+(.+)", text, re.S)
    if related_match:
        for slug in re.findall(r"`([a-z0-9-]+)`", related_match.group(1)):
            if slug not in known_slugs:
                errors.append(f"{rel}: unknown related skill `{slug}`")

    if "TODO" in text:
        errors.append(f"{rel}: contains TODO")

    return errors


def check_eval_suites(known_slugs: set[str]) -> list[str]:
    errors: list[str] = []
    if not EVALS_DIR.exists():
        errors.append("evals: missing eval directory")
        return errors

    seen_ids: set[str] = set()
    for path in sorted(EVALS_DIR.glob("*.json")):
        rel = path.relative_to(ROOT)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{rel}: invalid JSON: {exc}")
            continue

        queries = data.get("queries")
        if not isinstance(queries, list) or not queries:
            errors.append(f"{rel}: missing non-empty queries array")
            continue

        for index, row in enumerate(queries):
            prefix = f"{rel}: query[{index}]"
            query_id = row.get("id")
            if not query_id:
                errors.append(f"{prefix}: missing id")
            elif query_id in seen_ids:
                errors.append(f"{prefix}: duplicate id {query_id}")
            else:
                seen_ids.add(query_id)

            query_text = row.get("query", "")
            if len(query_text.split()) < 5:
                errors.append(f"{prefix}: query too short")

            for field in ("expected_skills", "acceptable_skills"):
                values = row.get(field, [])
                if not isinstance(values, list):
                    errors.append(f"{prefix}: {field} must be a list")
                    continue
                for slug in values:
                    if slug not in known_slugs:
                        errors.append(f"{prefix}: unknown {field} slug `{slug}`")

            departments = row.get("expected_departments", [])
            if not isinstance(departments, list):
                errors.append(f"{prefix}: expected_departments must be a list")
            elif row.get("expected_skills") and not departments:
                errors.append(f"{prefix}: positive eval needs expected_departments")

            if path.name == "app_build_queries.json":
                criteria = row.get("success_criteria", [])
                if not isinstance(criteria, list) or len(criteria) < 3:
                    errors.append(f"{prefix}: app eval needs at least three success criteria")

    if not seen_ids:
        errors.append("evals: no query ids found")
    return errors


def main() -> int:
    registry = load_registry()
    slugs = {row["slug"] for row in registry["skills"]}
    errors: list[str] = []

    for row in registry["skills"]:
        path = ROOT / row["path"]
        if not path.exists():
            errors.append(f"{row['slug']}: missing file {row['path']}")
            continue
        errors.extend(check_file(path, slugs))

    errors.extend(check_eval_suites(slugs))

    actual = {p.parent.name for p in SKILLS_DIR.glob("*/SKILL.md")}
    missing_registry = actual - slugs
    missing_dirs = slugs - actual
    for slug in sorted(missing_registry):
        errors.append(f"{slug}: skill folder missing from skills.json")
    for slug in sorted(missing_dirs):
        errors.append(f"{slug}: skills.json entry missing folder")

    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Skill validation passed for {len(slugs)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
