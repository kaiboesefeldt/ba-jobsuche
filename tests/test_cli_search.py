import contextlib
import io
import json
import unittest
from unittest.mock import patch

from ba_jobsuche.cli import main


class CliTests(unittest.TestCase):
    def test_search_produces_versioned_json(self):
        out = io.StringIO()
        with (
            patch("ba_jobsuche.cli.fetch_search", return_value={"maxErgebnisse": 0}),
            contextlib.redirect_stdout(out),
        ):
            status = main(["search", "--was", "Python"])
        data = json.loads(out.getvalue())
        self.assertEqual(status, 0)
        self.assertEqual(data["schema_version"], 1)
        self.assertEqual(data["results"], [])
        self.assertEqual(data["query"]["was"], "Python")

    def test_invalid_input_produces_json_error(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            status = main(["search", "--was", "Python", "--max-pages", "0"])
        self.assertNotEqual(status, 0)
        self.assertFalse(json.loads(out.getvalue())["ok"])

    def test_homeoffice_is_sent_only_when_requested(self):
        for options, expected in [
            ([], {"was": "Python"}),
            (["--homeoffice"], {"was": "Python", "arbeitszeit": "ho"}),
        ]:
            with self.subTest(options=options):
                out = io.StringIO()
                with (
                    patch(
                        "ba_jobsuche.cli.fetch_search",
                        return_value={"maxErgebnisse": 0},
                    ) as fetch,
                    contextlib.redirect_stdout(out),
                ):
                    status = main(["search", "--was", "Python", *options])
                self.assertEqual(status, 0)
                self.assertEqual(json.loads(out.getvalue())["query"], expected)
                self.assertEqual(
                    fetch.call_args.args[0], {**expected, "page": 1, "size": 100}
                )
