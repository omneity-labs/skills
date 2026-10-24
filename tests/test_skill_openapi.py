"""Check drift detection and the self-contained installed skill."""
import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from jsonschema import ValidationError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from skill_openapi import SKILL, check_live, generated, lint_skill, validate_example


class SkillBindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = json.loads((ROOT / "api/openapi.json").read_text())
        cls.bindings = json.loads((SKILL / "references/api-bindings.json").read_text())["references"]

    def test_all_operations_and_examples_are_bound(self):
        coverage = lint_skill(self.spec)
        self.assertEqual(coverage, {"operations": 39, "references": 14, "examples": 16, "websockets": 1})

    def test_wrong_body_field_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Undocumented request fields"):
            validate_example(self.spec, self.bindings["language-id.md"], "post_v1_language_identify", "application/json", "json",
                             '{"model":"gherbal-v4","input":"salam","text":"ignored typo"}')

    def test_missing_required_model_is_rejected(self):
        with self.assertRaises(ValidationError):
            validate_example(self.spec, self.bindings["language-id.md"], "post_v1_language_identify", "application/json", "json", '{"input":"salam"}')

    def test_invalid_enum_is_rejected(self):
        with self.assertRaises(ValidationError):
            validate_example(self.spec, self.bindings["language-encoding.md"], "post_v1_language_encode", "application/json", "json",
                             '{"model":"sawtone-v4","input":"dar","channel":"misspelled"}')

    def test_wrong_curl_file_field_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Undocumented request fields"):
            validate_example(self.spec, self.bindings["transcription.md"], "post_v1_speech_transcribe", "multipart/form-data", "bash",
                             'curl https://api.sawalni.com/v1/speech/transcribe -F file=@test.wav')

    def test_query_limit_and_required_parameter_are_checked(self):
        with self.assertRaises(ValidationError):
            validate_example(self.spec, self.bindings["maps.md"], "get_v1_atlas_search", "query", "bash",
                             'curl --get https://api.sawalni.com/v1/atlas/search --data q=Rabat --data limit=1000')
        with self.assertRaisesRegex(ValueError, "Missing query parameter q"):
            validate_example(self.spec, self.bindings["maps.md"], "get_v1_atlas_search", "query", "bash",
                             'curl --get https://api.sawalni.com/v1/atlas/search --data limit=5')

    def test_curl_method_or_path_cannot_disagree_with_binding(self):
        with self.assertRaisesRegex(ValueError, "curl method/path"):
            validate_example(self.spec, self.bindings["maps.md"], "get_v1_atlas_search", "query", "bash",
                             'curl --get https://api.sawalni.com/v1/atlas/route --data q=Rabat')

    def test_websocket_sample_cannot_drift(self):
        start = copy.deepcopy(self.spec["x-websocket"]["/v1/speech/transcribe/stream"]["start"])
        start["sample_rate"] = 24000
        with self.assertRaisesRegex(ValueError, "Invalid WebSocket sample_rate"):
            validate_example(self.spec, self.bindings["transcription.md"], "ws:/v1/speech/transcribe/stream", "start", "json", json.dumps(start))

    def test_removed_operation_fails_reference_generation(self):
        spec = copy.deepcopy(self.spec)
        del spec["paths"]["/v1/language/identify"]
        with self.assertRaisesRegex(ValueError, "unknown operationId"):
            generated(spec)

    def test_live_drift_requires_review(self):
        changed = copy.deepcopy(self.spec)
        changed["info"]["version"] = "changed"
        with self.assertRaisesRegex(ValueError, "differs from the pinned"):
            check_live(self.spec, fetch=lambda: changed)
        check_live(self.spec, fetch=lambda: self.spec)

    def test_install_has_no_repository_dependency_and_detects_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory) / "omneity"
            shutil.copytree(SKILL, installed, ignore=shutil.ignore_patterns("__pycache__"))
            helper = installed / "scripts/inspect_api.py"
            result = subprocess.run([sys.executable, "-I", str(helper), "post_v1_language_identify"], cwd=directory, check=True, capture_output=True, text=True)
            detail = json.loads(result.stdout)
            self.assertEqual(detail["path"], "/v1/language/identify")
            self.assertIn("IdentifyRequest", detail["components"]["schemas"])
            with (installed / "references/openapi.json").open("a") as stream:
                stream.write(" ")
            result = subprocess.run([sys.executable, "-I", str(helper), "post_v1_language_identify"], cwd=directory, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("does not match its lock", result.stderr)

    def test_unannotated_example_and_uncovered_operation_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory) / "omneity"
            shutil.copytree(SKILL, installed, ignore=shutil.ignore_patterns("__pycache__"))
            reference = installed / "references/language-id.md"
            original = reference.read_text()
            reference.write_text(original.replace("<!-- api-example: post_v1_language_identify application/json -->\n", ""))
            with self.assertRaisesRegex(ValueError, "unbound json example"):
                lint_skill(self.spec, installed)
            reference.write_text(original)
            bindings_path = installed / "references/api-bindings.json"
            bindings = json.loads(bindings_path.read_text())
            bindings["references"]["language-id.md"]["operations"] = []
            bindings_path.write_text(json.dumps(bindings))
            # Regenerate all artifacts so the missing binding itself is tested.
            for file, text in generated(self.spec, installed).items():
                file.write_text(text)
            reference.write_text(reference.read_text().split("Use `POST", 1)[0])
            with self.assertRaisesRegex(ValueError, "Uncovered OpenAPI operations"):
                lint_skill(self.spec, installed)


if __name__ == "__main__":
    unittest.main()
