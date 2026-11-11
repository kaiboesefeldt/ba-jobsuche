import runpy
import sys
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parents[1] / "skills/ba-jobsuche/scripts")
)

import contextlib
import io
import json
import unittest
from unittest.mock import patch

from ba_jobsuche.cli import main


class CliTests(unittest.TestCase):
    def test_help_explains_search_and_detail_inputs(self):
        for args, expected in (
            (
                ["search", "--help"],
                (
                    "Search terms",
                    "Location",
                    "1-100",
                    "default: 100",
                    "default: 10",
                    "100%",
                ),
            ),
            (["detail", "--help"], ("reference number",)),
        ):
            with (
                self.subTest(args=args),
                contextlib.redirect_stdout(io.StringIO()) as out,
            ):
                with self.assertRaises(SystemExit) as caught:
                    main(args)
                self.assertEqual(caught.exception.code, 0)
                for text in expected:
                    self.assertIn(text, out.getvalue())

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
            (["--homeoffice"], {"was": "Python", "homeoffice": "prozentual_100"}),
            *[
                (
                    ["--homeoffice", f"{value}%"],
                    {"was": "Python", "homeoffice": f"prozentual_{value}"},
                )
                for value in (0, 25, 50, 100)
            ],
            (
                ["--homeoffice", "--max-pages", "1"],
                {"was": "Python", "homeoffice": "prozentual_100"},
            ),
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
                reported = dict(expected)
                if "homeoffice" in reported:
                    reported["homeoffice"] = (
                        reported["homeoffice"].replace("prozentual_", "") + "%"
                    )
                self.assertEqual(json.loads(out.getvalue())["query"], reported)
                self.assertEqual(
                    fetch.call_args.args[0], {**expected, "page": 1, "size": 100}
                )

    def test_invalid_homeoffice_value_rejected_without_request(self):
        for value in ("10%", "50", "", "101%", "abc"):
            with (
                self.subTest(value=value),
                patch("ba_jobsuche.cli.fetch_search") as fetch,
                contextlib.redirect_stdout(io.StringIO()) as out,
            ):
                status = main(["search", "--was", "Python", "--homeoffice", value])
                self.assertEqual(status, 1)
                self.assertEqual(
                    json.loads(out.getvalue())["error"]["code"], "invalid_input"
                )
                fetch.assert_not_called()

    def test_location_and_nonempty_result(self):
        out = io.StringIO()
        response = {"maxErgebnisse": 1, "ergebnisliste": [{"referenznummer": "A"}]}
        with (
            patch("ba_jobsuche.cli.fetch_search", return_value=response) as fetch,
            contextlib.redirect_stdout(out),
        ):
            self.assertEqual(main(["search", "--was", "Python", "--wo", "Berlin"]), 0)
        self.assertEqual(
            fetch.call_args.args[0],
            {"was": "Python", "wo": "Berlin", "page": 1, "size": 100},
        )
        self.assertEqual(
            json.loads(out.getvalue())["query"], {"was": "Python", "wo": "Berlin"}
        )
        self.assertEqual(
            json.loads(out.getvalue())["results"], response["ergebnisliste"]
        )

    def test_location_radius_is_sent_and_reported(self):
        for value, location, radius in (
            ("Rostock:50", "Rostock", 50),
            ("Alt Ungnade:50", "Alt Ungnade", 50),
            ("Frankfurt (Oder):50", "Frankfurt (Oder)", 50),
            ("Berlin:0", "Berlin", 0),
            ("Berlin:200", "Berlin", 200),
            ("Berlin:00050", "Berlin", 50),
            ("Berlin:000", "Berlin", 0),
        ):
            with (
                self.subTest(value=value),
                patch(
                    "ba_jobsuche.cli.fetch_search", return_value={"maxErgebnisse": 0}
                ) as fetch,
                contextlib.redirect_stdout(io.StringIO()) as out,
            ):
                self.assertEqual(main(["search", "--was", "Python", "--wo", value]), 0)
                expected = {"was": "Python", "wo": location, "umkreis": radius}
                self.assertEqual(json.loads(out.getvalue())["query"], expected)
                self.assertEqual(
                    fetch.call_args.args[0], {**expected, "page": 1, "size": 100}
                )

    def test_invalid_radius_never_sends_request(self):
        for value in (
            ":50",
            " :50",
            "Berlin:",
            "Berlin:-1",
            "Berlin:201",
            "Berlin:1.5",
            "Berlin:9999",
            "Berlin:５０",
            "Berlin:abc",
            "Berlin:50:20",
            "Berlin: 50",
        ):
            with (
                self.subTest(value=value),
                patch("ba_jobsuche.cli.fetch_search") as fetch,
                contextlib.redirect_stdout(io.StringIO()) as out,
            ):
                self.assertEqual(main(["search", "--was", "Python", "--wo", value]), 1)
                self.assertEqual(
                    json.loads(out.getvalue())["error"]["code"], "invalid_input"
                )
                fetch.assert_not_called()

    def test_detail_success(self):
        out = io.StringIO()
        with (
            patch("ba_jobsuche.cli.fetch_detail", return_value={"titel": "Developer"}),
            contextlib.redirect_stdout(out),
        ):
            self.assertEqual(main(["detail", "ABC"]), 0)
        self.assertEqual(json.loads(out.getvalue())["result"]["titel"], "Developer")

    def test_bad_commands_and_arguments_are_json_errors(self):
        for args in (
            ["unknown"],
            ["search", "--was", "x", "--unexpected"],
            ["detail", " "],
        ):
            with (
                self.subTest(args=args),
                contextlib.redirect_stdout(io.StringIO()) as out,
            ):
                self.assertNotEqual(main(args), 0)
                self.assertFalse(json.loads(out.getvalue())["ok"])

    def test_dispatch_rejects_unsupported_command(self):
        from argparse import Namespace

        from ba_jobsuche.cli import dispatch

        with self.assertRaises(ValueError):
            dispatch(Namespace(command="unknown"))

    def test_service_and_validation_errors(self):
        from ba_jobsuche.api import ApiError

        cases = [
            (["search", "--was", " "], None, "invalid_input"),
            (["search", "--was", "x", "--wo", " "], None, "invalid_input"),
            (["detail", "x"], [], "invalid_response"),
            (["detail", "x"], ApiError("network_error", "failed"), "network_error"),
        ]
        for args, response, code in cases:
            with (
                self.subTest(args=args, code=code),
                contextlib.redirect_stdout(io.StringIO()) as out,
            ):
                with patch(
                    "ba_jobsuche.cli.fetch_detail",
                    side_effect=response if isinstance(response, Exception) else None,
                    return_value=response,
                ):
                    self.assertEqual(main(args), 1)
                self.assertEqual(json.loads(out.getvalue())["error"]["code"], code)

    def test_module_entrypoint_returns_command_status(self):
        import runpy

        with (
            patch("ba_jobsuche.cli.main", return_value=7),
            self.assertRaises(SystemExit) as caught,
        ):
            runpy.run_module("ba_jobsuche", run_name="__main__")
        self.assertEqual(caught.exception.code, 7)


class ScriptEntrypointTests(unittest.TestCase):
    def test_script_entrypoint_returns_command_status(self):
        script = (
            Path(__file__).resolve().parents[1]
            / "skills/ba-jobsuche/scripts/jobsuche.py"
        )
        with (
            patch("ba_jobsuche.cli.main", return_value=7),
            self.assertRaises(SystemExit) as caught,
        ):
            runpy.run_path(str(script), run_name="__main__")
        self.assertEqual(caught.exception.code, 7)
