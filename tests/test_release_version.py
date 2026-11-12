import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_release.py"


class ReleaseVersionTests(unittest.TestCase):
    def check(self, previous, current, notes="Changes"):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "version").write_text(current)
            (root / "notes").write_text(notes)
            command = [
                "python3",
                str(SCRIPT),
                str(root / "version"),
                str(root / "notes"),
            ]
            if previous is not None:
                command += ["--previous", previous]
            return subprocess.run(command, capture_output=True, text=True, check=False)

    def test_initial_release_and_numeric_order(self):
        for previous, current in [
            (None, "1.0.0"),
            ("1.9.9", "1.10.0"),
            ("1.2.9", "2.0.0"),
        ]:
            with self.subTest(previous=previous, current=current):
                self.assertEqual(self.check(previous, current).returncode, 0)

    def test_rejects_invalid_bootstrap_and_versions(self):
        for previous, current in [
            (None, "1.0.1"),
            ("1.0.0", "1.0.0"),
            ("2.0.0", "1.9.9"),
            ("1.0.0", "1.01.0"),
            ("1.0.0", "1.0.1-rc1"),
            ("broken", "1.0.1"),
        ]:
            with self.subTest(previous=previous, current=current):
                self.assertNotEqual(self.check(previous, current).returncode, 0)

    def test_rejects_empty_release_notes(self):
        self.assertNotEqual(self.check("1.0.0", "1.0.1", " \n").returncode, 0)


if __name__ == "__main__":
    unittest.main()
