import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class SkillBundleTest(unittest.TestCase):
    def test_isolated_skill_runs_from_another_directory(self):
        source = Path(__file__).resolve().parents[1] / "skills" / "ba-jobsuche"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "installed skill"
            shutil.copytree(source, skill, ignore=shutil.ignore_patterns("__pycache__"))
            environment = os.environ.copy()
            environment.pop("PYTHONPATH", None)
            result = subprocess.run(
                [sys.executable, str(skill / "scripts" / "jobsuche.py"), "detail", ""],
                cwd=root,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(json.loads(result.stdout)["error"]["code"], "invalid_input")

    def test_isolated_search_and_detail_with_stubbed_api(self):
        source = Path(__file__).resolve().parents[1] / "skills" / "ba-jobsuche"
        harness = """
import json, runpy, sys
from unittest.mock import patch
sys.path.insert(0, sys.argv[1])
script, command = sys.argv[2:]
sys.argv = [script] + (['search', '--was', 'Developer'] if command == 'search' else ['detail', 'REF'])
with patch('ba_jobsuche.cli.fetch_search', return_value={'maxErgebnisse': 0}), patch('ba_jobsuche.cli.fetch_detail', return_value={'titel': 'Developer'}):
    runpy.run_path(script, run_name='__main__')
"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "installed skill"
            shutil.copytree(source, skill, ignore=shutil.ignore_patterns("__pycache__"))
            script = skill / "scripts" / "jobsuche.py"
            environment = os.environ.copy()
            environment.pop("PYTHONPATH", None)
            for command in ("search", "detail"):
                with self.subTest(command=command):
                    result = subprocess.run(
                        [
                            sys.executable,
                            "-c",
                            harness,
                            str(script.parent),
                            str(script),
                            command,
                        ],
                        cwd=root,
                        env=environment,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    output = json.loads(result.stdout)
                    self.assertTrue(output["ok"])
                    self.assertEqual(output["schema_version"], 1)
                    if command == "search":
                        self.assertEqual(output["results"], [])
                    else:
                        self.assertEqual(output["result"]["titel"], "Developer")
