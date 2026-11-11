import base64
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

SPEC = importlib.util.spec_from_file_location(
    "github_app", Path(__file__).resolve().parents[1] / "scripts" / "github_app.py"
)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class GitHubAppTests(unittest.TestCase):
    def test_sign_uses_rsa_sha256_without_external_process(self):
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        pem = key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "key.pem"
            path.write_bytes(pem)
            with patch.object(
                module.subprocess, "run", side_effect=AssertionError("external process")
            ):
                signature = module.sign(b"message", path)
        key.public_key().verify(
            signature, b"message", padding.PKCS1v15(), hashes.SHA256()
        )

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

    def test_git_environment_does_not_inherit_github_tokens(self):
        with patch.dict(
            os.environ, {"GH_TOKEN": "old", "GITHUB_TOKEN": "old2"}, clear=True
        ):
            git_env = module.git_environment("secret")
        self.assertNotIn("GH_TOKEN", git_env)
        self.assertEqual(
            git_env["GIT_CONFIG_KEY_0"], "http.https://github.com/.extraheader"
        )
        self.assertNotIn("secret", git_env["GIT_CONFIG_VALUE_0"])

    def test_api_request_uses_github_and_bearer_token(self):
        with patch.object(
            module, "open_request", return_value=b'{"ok":true}'
        ) as opener:
            result = module.api_request("secret", "/repos/example/project", "GET", None)
        self.assertEqual(result, b'{"ok":true}')
        request = opener.call_args.args[0]
        self.assertEqual(
            request.full_url, "https://api.github.com/repos/example/project"
        )
        self.assertEqual(request.get_header("Authorization"), "Bearer secret")

    def test_api_rejects_external_url(self):
        with self.assertRaises(ValueError):
            module.api_request("secret", "//example.com/steal", "GET", None)

    def test_request_rejects_invalid_response(self):
        with (
            patch.object(module, "open_request", return_value=b'{"token": 42}'),
            self.assertRaisesRegex(ValueError, "token"),
        ):
            module.installation_token("jwt", "123")


if __name__ == "__main__":
    unittest.main()
