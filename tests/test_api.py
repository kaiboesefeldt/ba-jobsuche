import sys
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parents[1] / "skills/ba-jobsuche/scripts")
)

import io
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from ba_jobsuche.api import ApiError, fetch_detail, fetch_search


class ApiTests(unittest.TestCase):
    def test_search_encodes_parameters_and_public_key(self):
        with patch(
            "ba_jobsuche.api.urlopen", return_value=io.BytesIO(b'{"maxErgebnisse": 0}')
        ) as call:
            self.assertEqual(
                fetch_search({"was": "C++", "page": 1}), {"maxErgebnisse": 0}
            )
        request = call.call_args.args[0]
        self.assertIn("was=C%2B%2B", request.full_url)
        self.assertEqual(request.get_header("X-api-key"), "jobboerse-jobsuche")

    def test_detail_encodes_reference(self):
        with patch("ba_jobsuche.api.urlopen", return_value=io.BytesIO(b"{}")) as call:
            fetch_detail("abc")
        self.assertTrue(call.call_args.args[0].full_url.endswith("/YWJj"))

    def test_http_error_does_not_expose_response(self):
        error = HTTPError("https://example.com", 403, "secret", {}, None)
        with (
            patch("ba_jobsuche.api.urlopen", side_effect=error),
            self.assertRaises(ApiError) as caught,
        ):
            fetch_search({})
        self.assertEqual(caught.exception.code, "http_error")
        self.assertNotIn("secret", str(caught.exception))
        error.close()

    def test_invalid_json_and_network_failure(self):
        from urllib.error import URLError

        for failure, code in [
            (io.BytesIO(b"not json"), "invalid_response"),
            (URLError("offline"), "network_error"),
        ]:
            with self.subTest(code=code):
                kwargs = (
                    {"side_effect": failure}
                    if isinstance(failure, Exception)
                    else {"return_value": failure}
                )
                with (
                    patch("ba_jobsuche.api.urlopen", **kwargs),
                    self.assertRaises(ApiError) as caught,
                ):
                    fetch_search({"was": "Python"})
                self.assertEqual(caught.exception.code, code)
