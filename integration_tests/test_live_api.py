"""Opt-in integration tests against the live BA Jobsuche API."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills/ba-jobsuche/scripts/jobsuche.py"


class LiveApiTests(unittest.TestCase):
    def run_cli(self, *args):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        result = json.loads(completed.stdout)
        self.assertTrue(result["ok"], result)
        return result

    def search(self, *options):
        result = self.run_cli(
            "search",
            "--was",
            "Softwareentwickler",
            "--size",
            "3",
            "--max-pages",
            "1",
            *options,
        )
        self.assertTrue(result["results"], "Live search returned no results")
        return result

    def detail(self, reference):
        result = self.run_cli("detail", reference)
        self.assertEqual(result["reference"], reference)
        self.assertTrue(result["result"], "Live detail response is empty")
        self.assertEqual(result["result"].get("referenznummer"), reference)
        return result["result"]

    def test_search_and_detail_happy_path(self):
        result = self.search()
        self.detail(result["results"][0]["referenznummer"])

    def test_homeoffice_results_have_homeoffice_in_details(self):
        result = self.search("--homeoffice", "100%")
        self.assertEqual(result["query"]["homeoffice"], "prozentual_100")
        for entry in result["results"]:
            with self.subTest(reference=entry["referenznummer"]):
                detail = self.detail(entry["referenznummer"])
                self.assertIs(detail.get("homeofficemoeglich"), True, detail)
                self.assertGreaterEqual(
                    detail.get("homeofficeprozent", -1), 100, detail
                )


if __name__ == "__main__":
    unittest.main()
