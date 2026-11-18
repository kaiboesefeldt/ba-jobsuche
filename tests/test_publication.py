import contextlib
import io
import json
import sys
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

sys.path.insert(
    0, str(Path(__file__).resolve().parents[1] / "skills/ba-jobsuche/scripts")
)
from ba_jobsuche.cli import main
from ba_jobsuche.search import order_publications


class PublicationTests(unittest.TestCase):
    def test_filter_sort_and_unknown_dates(self):
        entries = [
            {"referenznummer": "old", "datumErsteVeroeffentlichung": "2026-11-15"},
            {"referenznummer": "edge", "datumErsteVeroeffentlichung": "2026-11-16"},
            {
                "referenznummer": "unknown",
                "datumErsteVeroeffentlichung": "bad",
                "aktuelleVeroeffentlichung": "2026-11-18",
            },
            {"referenznummer": "new", "datumErsteVeroeffentlichung": "2026-11-18"},
            {"referenznummer": "tie", "datumErsteVeroeffentlichung": "2026-11-18"},
            {"referenznummer": "missing"},
        ]
        result, unknown = order_publications(entries, 2, date(2026, 11, 18))
        self.assertEqual(
            [e["referenznummer"] for e in result],
            ["new", "tie", "edge", "unknown", "missing"],
        )
        self.assertEqual(unknown, 2)

    def test_api_prefilter_and_output(self):
        for age, expected in [
            (0, 0),
            (1, 1),
            (2, 7),
            (8, 14),
            (15, 28),
            (29, None),
            (100, None),
        ]:
            with (
                self.subTest(age=age),
                patch(
                    "ba_jobsuche.cli.fetch_search", return_value={"maxErgebnisse": 0}
                ) as fetch,
                contextlib.redirect_stdout(io.StringIO()) as out,
            ):
                self.assertEqual(
                    main(
                        ["search", "--was", "Python", "--veroeffentlichtseit", str(age)]
                    ),
                    0,
                )
                params = fetch.call_args.args[0]
                self.assertEqual(params.get("veroeffentlichtseit"), expected)
                self.assertEqual(params["sort"], "veroeffdatum")
                self.assertEqual(
                    json.loads(out.getvalue())["query"]["veroeffentlichtseit"], age
                )
                self.assertNotIn(
                    "unknown_publication_dates", json.loads(out.getvalue())
                )

    def test_combined_search_filters_after_all_pages_and_sorts_globally(self):
        pages = {
            ("a", 1): [
                {"referenznummer": "older", "datumErsteVeroeffentlichung": "2026-11-16"}
            ],
            ("a", 2): [
                {"referenznummer": "old", "datumErsteVeroeffentlichung": "2026-11-15"}
            ],
            ("b", 1): [
                {"referenznummer": "new", "datumErsteVeroeffentlichung": "2026-11-18"}
            ],
            ("b", 2): [{"referenznummer": "unknown"}],
        }

        def fetch(params):
            return {
                "maxErgebnisse": 2,
                "ergebnisliste": pages[(params["was"], params["page"])],
            }

        class Clock:
            @staticmethod
            def now(zone):
                from datetime import datetime

                return datetime(2026, 11, 18, 0, 30, tzinfo=zone)

        with (
            patch("ba_jobsuche.cli.fetch_search", side_effect=fetch),
            patch("ba_jobsuche.cli.datetime", Clock),
            contextlib.redirect_stdout(io.StringIO()) as out,
            contextlib.redirect_stderr(io.StringIO()) as err,
        ):
            self.assertEqual(
                main(
                    [
                        "search",
                        "--was",
                        "a",
                        "--was",
                        "b",
                        "--size",
                        "1",
                        "--veroeffentlichtseit",
                        "2",
                    ]
                ),
                0,
            )
        result = json.loads(out.getvalue())
        self.assertEqual(
            [entry["referenznummer"] for entry in result["results"]],
            ["new", "older", "unknown"],
        )
        self.assertEqual(result["pages_fetched"], 4)
        self.assertIn("1 results", err.getvalue())
        self.assertTrue(result["complete"])

    def test_berlin_date_without_timezone_database(self):
        from datetime import datetime, timezone

        from ba_jobsuche.cli import berlin_date

        for instant, expected in [
            (datetime(2026, 1, 1, 23, 30, tzinfo=timezone.utc), date(2026, 1, 2)),
            (datetime(2026, 7, 1, 22, 30, tzinfo=timezone.utc), date(2026, 7, 2)),
            (datetime(2026, 3, 29, 0, 30, tzinfo=timezone.utc), date(2026, 3, 29)),
        ]:
            with (
                self.subTest(instant=instant),
                patch("ba_jobsuche.cli.ZoneInfo", side_effect=KeyError),
            ):
                self.assertEqual(berlin_date(instant), expected)

    def test_oldest_valid_date_precedes_unknown_without_filter(self):
        entries = [
            {"referenznummer": "unknown"},
            {"referenznummer": "valid", "datumErsteVeroeffentlichung": "0001-01-01"},
        ]
        result, _ = order_publications(entries, None, date(2026, 11, 18))
        self.assertEqual(
            [entry["referenznummer"] for entry in result], ["valid", "unknown"]
        )
