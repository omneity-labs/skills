"""Contract regressions: reject known wrong shapes and detect broken artifacts."""
import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from api_contract import build
from generate_openapi import artifacts
from lint_openapi import lint


class ContractTests(unittest.TestCase):
    def test_known_invalid_requests_are_rejected(self):
        schemas = build()["components"]["schemas"]
        for name, payload in [
            ("IdentifyRequest", {"text": "salam"}),
            ("EncodeRequest", {"model": "sawtone-v4", "text": "dar"}),
            ("RhymeScoreRequest", {"word_a": "rain", "word_b": "train"}),
            ("RhymeScoreRequest", {"pairs": [["rain", "train", "plain"]]}),
            ("LyricScoreRequest", {"lines": ["rain", "train"], "language": "eng_Latn"}),
            ("TarakibRequest", {"text": "hello", "tokens": ["hello"]}),
            ("TarakibRequest", {}),
        ]:
            with self.subTest(name=name, payload=payload), self.assertRaises(ValidationError):
                Draft202012Validator(schemas[name]).validate(payload)

    def test_valid_batch_and_multipart_shapes(self):
        schemas = build()["components"]["schemas"]
        for name, payload in [
            ("IdentifyRequest", {"model": "gherbal-v4", "input": ["salam", "hello"], "top": 3}),
            ("RhymeScoreRequest", {"pairs": [["rain", "train"]]}),
            ("TarakibRequest", {"tokens": ["hello", "world"]}),
            ("AlignmentRequest", {"audio": "binary", "text": "hello"}),
            ("TranscribeRequest", {"audio": "binary", "model": "daktilo", "language": "ar"}),
        ]:
            Draft202012Validator(schemas[name]).validate(payload)

    def test_generated_artifacts_are_current(self):
        for path, content in artifacts().items():
            self.assertEqual(path.read_text(), content, str(path))

    def test_broken_reference_fails_validation(self):
        spec = copy.deepcopy(build())
        spec["paths"]["/v1/models"]["get"]["responses"]["200"]["content"]["application/json"]["schema"] = {"$ref": "#/components/schemas/Missing"}
        with tempfile.TemporaryDirectory() as directory, self.assertRaises(Exception):
            lint(spec, Path(directory))

    def test_private_routes_are_absent(self):
        spec = build()
        self.assertFalse(any(path.startswith("/v1/admin/") or path == "/healthz" for path in spec["paths"]))
        self.assertEqual(spec["x-websocket"]["/v1/speech/transcribe/stream"]["protocol"], "sawalni.transcribe.v1")
        self.assertNotIn("/v1/speech/transcribe/stream", spec["paths"])

    def test_auth_is_distinct(self):
        spec = build()
        self.assertEqual(spec["paths"]["/api/public/knowledge/{id}/search"]["post"]["security"], [{"KnowledgeKey": []}])
        self.assertNotIn("/api/public/chatbots/{slug}/chat", spec["paths"])
        self.assertNotIn("/v1/demo/asat", spec["paths"])


if __name__ == "__main__":
    unittest.main()
