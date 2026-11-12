import contextlib
import copy
import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from jsonschema import Draft202012Validator

SKILL = Path(__file__).resolve().parents[1] / "skills" / "ba-jobsuche"
sys.path.insert(0, str(SKILL / "scripts"))

from ba_jobsuche.cli import main


class OutputSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(
            (SKILL / "references" / "output.schema.json").read_text()
        )
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(
            cls.schema, format_checker=Draft202012Validator.FORMAT_CHECKER
        )

    def output(self, args, search_response=None, detail_response=None):
        with (
            patch("ba_jobsuche.cli.fetch_search", return_value=search_response),
            patch("ba_jobsuche.cli.fetch_detail", return_value=detail_response),
            contextlib.redirect_stdout(io.StringIO()) as out,
        ):
            main(args)
        return json.loads(out.getvalue())

    def test_actual_search_detail_and_error_outputs_validate(self):
        outputs = [
            self.output(["search", "--was", "x"], {"maxErgebnisse": 0}),
            self.output(
                ["search", "--was", "x", "--was", "y", "--wo", "A:50", "--wo", "B"],
                {"maxErgebnisse": 0},
            ),
            self.output(
                ["search", "--was", "x", "--wo", "Rostock:50", "--homeoffice"],
                {"maxErgebnisse": 0},
            ),
            self.output(
                ["search", "--was", "x", "--max-pages", "1"],
                {
                    "maxErgebnisse": 101,
                    "ergebnisliste": [{"referenznummer": "A", "future": {"any": 1}}],
                },
            ),
            self.output(
                ["search", "--was", "x"], {"maxErgebnisse": 1, "ergebnisliste": []}
            ),
            self.output(["detail", "A"], detail_response={"future": [1, None]}),
            self.output(["detail", ""]),
        ]
        for output in outputs:
            with self.subTest(output=output):
                self.validator.validate(output)

    def test_skill_examples_match_schema(self):
        skill_text = (SKILL / "SKILL.md").read_text()
        examples = [
            json.loads(part.split("\n```", 1)[0])
            for part in skill_text.split("```json\n")[1:]
        ]
        self.assertEqual(len(examples), 2)
        for example in examples:
            self.validator.validate(example)
        self.assertTrue(examples[0]["results"])
        self.assertTrue(examples[1]["result"])

    def test_invalid_envelopes_are_rejected(self):
        valid = self.output(["search", "--was", "x"], {"maxErgebnisse": 0})
        cases = []
        missing = copy.deepcopy(valid)
        del missing["results"]
        cases.append(missing)
        inconsistent = copy.deepcopy(valid)
        inconsistent["complete"] = False
        cases.append(inconsistent)
        wrong_version = copy.deepcopy(valid)
        wrong_version["schema_version"] = 2
        cases.append(wrong_version)
        cases.append(
            {"schema_version": 1, "ok": False, "error": {"code": 12, "message": "x"}}
        )
        for case in cases:
            with self.subTest(case=case):
                self.assertFalse(self.validator.is_valid(case))
