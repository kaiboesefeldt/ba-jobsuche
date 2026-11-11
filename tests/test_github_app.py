import base64
import importlib.util
import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "github_app", Path(__file__).resolve().parents[1] / "scripts" / "github_app.py"
)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class GitHubAppTests(unittest.TestCase):
    def test_jwt_has_expected_claims_and_signature(self):
        with (
            patch.object(module.time, "time", return_value=1000),
            patch.object(module, "sign", return_value=b"signed"),
        ):
            jwt = module.create_jwt("123", Path("key"))
        header, payload, signature = jwt.split(".")

        def decode(part):
            return base64.urlsafe_b64decode(part + "=" * (-len(part) % 4))

        self.assertEqual(json.loads(decode(header)), {"alg": "RS256", "typ": "JWT"})
        self.assertEqual(
            json.loads(decode(payload)), {"iat": 940, "exp": 1540, "iss": "123"}
        )
        self.assertEqual(decode(signature), b"signed")

    def test_child_environment_is_scoped_to_selected_tool(self):
        with patch.dict(
            os.environ, {"GH_TOKEN": "old", "GITHUB_TOKEN": "old2"}, clear=True
        ):
            gh_env = module.child_environment("gh", "secret")
            git_env = module.child_environment("git", "secret")
        self.assertEqual(gh_env["GH_TOKEN"], "secret")
        self.assertNotIn("GITHUB_TOKEN", gh_env)
        self.assertNotIn("GH_TOKEN", git_env)
        self.assertEqual(
            git_env["GIT_CONFIG_KEY_0"], "http.https://github.com/.extraheader"
        )
        self.assertNotIn("secret", git_env["GIT_CONFIG_VALUE_0"])
        self.assertNotIn("GIT_CONFIG_VALUE_0", gh_env)

    def test_request_rejects_invalid_response(self):
        with patch.object(module.urllib.request, "urlopen") as urlopen:
            urlopen.return_value.__enter__.return_value.read.return_value = (
                b'{"token": 42}'
            )
            with self.assertRaisesRegex(ValueError, "token"):
                module.installation_token("jwt", "123")


if __name__ == "__main__":
    unittest.main()
