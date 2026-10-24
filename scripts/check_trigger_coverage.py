#!/usr/bin/env python3
"""Score Omneity skill trigger and department-routing evals.

Default mode is a deterministic keyword baseline that catches obvious coverage
holes. For real model/router evals, pass a predictions JSON file with either:

{
  "query-id": {
    "predicted_skills": ["omneity"],
    "predicted_departments": ["chat", "app-patterns"]
  }
}

or:

[
  {
    "id": "query-id",
    "predicted_skills": ["omneity"],
    "predicted_departments": ["chat"]
  }
]
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "skills.json"
EVALS_DIR = ROOT / "evals"

DEPARTMENTS = {
    "functionality",
    "chat",
    "embeddings",
    "language-id",
    "language-encoding",
    "rhyme-lyrics",
    "transcription",
    "text-alignment",
    "herd",
    "semango",
    "app-patterns",
}

OMNEITY_PATTERNS = (
    r"\bomneity\b",
    r"\bsawalni\b",
    r"\bsawtone\b",
    r"\bziryab\b",
    r"\bdaktilo\b",
    r"\bsawalign\b",
    r"\bherd\b",
    r"\bsemango\b",
    r"\bchat\b",
    r"\bassistant\b",
    r"\bchatbot\b",
    r"\bembedding",
    r"\bvector",
    r"\brag\b",
    r"\blanguage\b",
    r"\bdialect\b",
    r"\barabizi\b",
    r"\bcross-script\b",
    r"\bphonetic\b",
    r"\brhyme\b",
    r"\blyric",
    r"\btranscrib",
    r"\bspeech-to-text\b",
    r"\bsubtitle",
    r"\balign",
    r"\btrail\b",
    r"\bbrowser automation\b",
    r"\bself-host",
    r"\bhybrid search\b",
    r"\blocal search\b",
)

DEPARTMENT_RULES: dict[str, tuple[str, ...]] = {
    "functionality": (
        r"\bwhich\b.*\bcapabilit",
        r"\bwhat\b.*\bapi\b",
        r"\bchoose\b.*\bapi\b",
        r"\bmap\b.*\bdepartments\b",
        r"\bproduct names\b",
        r"\bhosted ai\b.*\bbrowser automation\b.*\blocal search\b",
    ),
    "chat": (
        r"\bchat\b",
        r"\bassistant\b",
        r"\bchatbot\b",
        r"\btranslation-like\b",
        r"\bstructured json\b",
        r"\bcompletion\b",
        r"\banswer\b",
        r"\bsummar",
        r"\bhosted ai\b",
        r"\bmodel prompts\b",
    ),
    "embeddings": (
        r"\bembedding",
        r"\bvector",
        r"\brag\b",
        r"\bdeduplicate\b",
        r"\bcluster\b",
        r"\bhosted-vector\b",
    ),
    "language-id": (
        r"\blanguage detection\b",
        r"\bdetect\b.*\blanguage\b",
        r"\bdetected language\b",
        r"\bclassify\b.*\bscript\b",
        r"\bdialect\b",
        r"\barabizi\b",
        r"\bconfidence scores\b",
    ),
    "language-encoding": (
        r"\bencode\b",
        r"\bcross-script\b",
        r"\barabic\b.*\blatin\b",
        r"\blatin\b.*\barabic\b",
        r"\bfuzzy\b",
        r"\bphonetic\b",
        r"\btypo-resistant\b",
        r"\bspellings\b",
    ),
    "rhyme-lyrics": (
        r"\brhyme\b",
        r"\blyric",
        r"\bsongwriting\b",
        r"\bsong\b",
    ),
    "transcription": (
        r"\btranscrib",
        r"\bspeech-to-text\b",
        r"\bvoice notes?\b",
        r"\baudio files?\b",
        r"\buploaded file\b",
        r"\bpodcast audio\b",
        r"\bvideo audio\b",
    ),
    "text-alignment": (
        r"\balign\b",
        r"\bsubtitles?\b",
        r"\bsrt\b",
        r"\bvtt\b",
        r"\bpremiere\b",
        r"\btiming\b",
        r"\btimeline\b",
        r"\bline up\b",
    ),
    "herd": (
        r"\bherd\b",
        r"\btrails?\b",
        r"\bbrowser automation\b",
        r"\bautomate\b.*\bwebsite\b",
        r"\bwebsite\b.*\bautomation\b",
        r"\bregistry\b",
        r"\bselector",
        r"\bdom\b",
        r"\bdevices?\b",
        r"\brpc\b",
        r"\bevent stream\b",
        r"\bcli\b.*\bjson params\b",
    ),
    "semango": (
        r"\bsemango\b",
        r"\bself-host",
        r"\blocal search\b",
        r"\bsearch docs\b",
        r"\bhybrid search\b",
        r"\bprivate\b.*\bknowledge",
        r"\bprivate docs\b",
        r"\bprivate\b.*\bfiles\b",
        r"\bown server\b",
        r"\bindex\b.*\bdocs\b",
        r"\bindex\b.*\brepository\b",
        r"\bindex\b.*\blocally\b",
        r"\bcollected files\b",
        r"\binclude\b.*\bexclude\b.*\bglob",
        r"\bpdfs?\b.*\bmarkdown\b",
    ),
    "app-patterns": (
        r"\bbackend\b",
        r"\bserver-side\b",
        r"\bapi key\b",
        r"\bretry",
        r"\btimeouts?\b",
        r"\buser-facing\b",
        r"\bstatus\b",
        r"\bdashboard\b",
    ),
}



# Current hosted API departments. Keep these rules separate from the model eval.
DEPARTMENT_RULES.update({
    "translation": (r"\btarjamli\b", r"\bdedicated translation\b"),
    "rescript": (r"\brescript\b", r"\btransliteration\b", r"\bscript conversion\b"),
    "speech-synthesis": (r"\basat\b", r"\btext-to-speech\b", r"\bspeech synthesis\b"),
    "grammar": (r"\btarakib\b", r"\bmorphology\b", r"\bdependency parsing\b"),
    "knowledge-search": (r"\bmaktaba\b", r"\bakhbar\b", r"\bkhizana\b", r"\bbatbot\b"),
    "maps": (r"\batlas\b", r"\bdriving routes\b"),
    "pricing": (r"\bpricing\b", r"\bbilling units\b", r"\brate card\b"),
})
DEPARTMENTS.update(DEPARTMENT_RULES)

@dataclass(frozen=True)
class Query:
    id: str
    query: str
    expected_skills: set[str]
    expected_departments: set[str]


@dataclass(frozen=True)
class Prediction:
    skills: set[str]
    departments: set[str]


def load_registry() -> set[str]:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return {row["slug"] for row in data["skills"]}


def load_queries(paths: list[Path]) -> list[Query]:
    rows: list[Query] = []
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        for row in data.get("queries", []):
            rows.append(
                Query(
                    id=row["id"],
                    query=row["query"],
                    expected_skills=set(row.get("expected_skills", [])),
                    expected_departments=set(row.get("expected_departments", [])),
                )
            )
    return rows


def heuristic_predict(query: str) -> Prediction:
    text = query.lower()
    departments = {
        department
        for department, patterns in DEPARTMENT_RULES.items()
        if any(re.search(pattern, text) for pattern in patterns)
    }
    skills = {"omneity"} if departments or any(re.search(pattern, text) for pattern in OMNEITY_PATTERNS) else set()

    if "not a self-hosted" in text or "not self-hosted" in text:
        departments.discard("semango")
    if "transcript alignment" in text and "not transcript alignment" in text:
        departments.discard("text-alignment")

    return Prediction(skills=skills, departments=departments)


def normalize_prediction(value) -> Prediction:
    if isinstance(value, list):
        return Prediction(skills=set(value), departments=set())
    if isinstance(value, dict):
        return Prediction(
            skills=set(value.get("predicted_skills", [])),
            departments=set(value.get("predicted_departments", [])),
        )
    return Prediction(skills=set(), departments=set())


def load_predictions(path: Path) -> dict[str, Prediction]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return {key: normalize_prediction(value) for key, value in data.items()}
    return {row["id"]: normalize_prediction(row) for row in data}


def score(queries: list[Query], predictions: dict[str, Prediction], known: set[str]) -> tuple[int, list[str]]:
    failures: list[str] = []
    total = len(queries)
    skill_exact = 0
    skill_recall = 0
    skill_precision = 0
    department_exact = 0
    department_recall = 0
    department_precision = 0

    for query in queries:
        predicted = predictions.get(query.id, Prediction(set(), set()))
        unknown_skills = predicted.skills - known
        unknown_departments = predicted.departments - DEPARTMENTS
        if unknown_skills:
            failures.append(f"{query.id}: unknown predicted skills {sorted(unknown_skills)}")
        if unknown_departments:
            failures.append(f"{query.id}: unknown predicted departments {sorted(unknown_departments)}")

        missing_skills = query.expected_skills - predicted.skills
        extra_skills = predicted.skills - query.expected_skills
        expected_departments = query.expected_departments
        predicted_departments = predicted.departments
        if not expected_departments:
            predicted_departments = set()
        missing_departments = expected_departments - predicted_departments

        if not missing_skills:
            skill_recall += 1
        if not extra_skills:
            skill_precision += 1
        if predicted.skills == query.expected_skills:
            skill_exact += 1

        if not missing_departments:
            department_recall += 1
        if not missing_departments:
            department_precision += 1
        if not missing_departments:
            department_exact += 1

        if missing_skills or extra_skills or missing_departments:
            failures.append(
                f"{query.id}: expected_skills={sorted(query.expected_skills)} "
                f"predicted_skills={sorted(predicted.skills)} "
                f"missing_skills={sorted(missing_skills)} extra_skills={sorted(extra_skills)} "
                f"expected_departments={sorted(expected_departments)} "
                f"predicted_departments={sorted(predicted_departments)} "
                f"missing_departments={sorted(missing_departments)} "
            )

    print(f"Queries: {total}")
    print(f"Skill exact: {skill_exact}/{total}")
    print(f"Skill recall pass: {skill_recall}/{total}")
    print(f"Skill precision pass: {skill_precision}/{total}")
    print(f"Department exact: {department_exact}/{total}")
    print(f"Department recall pass: {department_recall}/{total}")
    print(f"Department precision pass: {department_precision}/{total}")

    return 0 if not failures else 1, failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Omneity skill trigger coverage")
    parser.add_argument(
        "--suite",
        action="append",
        default=[],
        help="Eval suite path. Defaults to trigger and app-build suites.",
    )
    parser.add_argument("--predictions", help="Optional predictions JSON to score")
    parser.add_argument("--json", action="store_true", help="Print failure JSON")
    args = parser.parse_args()

    suite_paths = [Path(p) for p in args.suite] if args.suite else [
        EVALS_DIR / "trigger_queries.json",
        EVALS_DIR / "app_build_queries.json",
    ]
    known = load_registry()
    queries = load_queries(suite_paths)

    if args.predictions:
        predictions = load_predictions(Path(args.predictions))
    else:
        predictions = {query.id: heuristic_predict(query.query) for query in queries}

    status, failures = score(queries, predictions, known)
    if failures:
        if args.json:
            print(json.dumps({"failures": failures}, indent=2))
        else:
            print("Failures:")
            for failure in failures:
                print(f"  - {failure}")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
