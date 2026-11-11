import unittest

from ba_jobsuche.search import search


class SearchTests(unittest.TestCase):
    def test_pages_are_deduplicated_and_exhausted(self):
        pages = [
            {
                "maxErgebnisse": 3,
                "ergebnisliste": [{"referenznummer": "a"}, {"referenznummer": "b"}],
            },
            {
                "maxErgebnisse": 3,
                "ergebnisliste": [{"referenznummer": "b"}, {"referenznummer": "c"}],
            },
        ]
        result = search(lambda params: pages[params["page"] - 1], {}, 2, 10)
        self.assertEqual(
            [x["referenznummer"] for x in result["results"]], ["a", "b", "c"]
        )
        self.assertEqual(result["stop_reason"], "exhausted")

    def test_limit_is_explicit(self):
        result = search(
            lambda _: {"maxErgebnisse": 20, "ergebnisliste": [{"referenznummer": "a"}]},
            {},
            1,
            1,
        )
        self.assertEqual(result["stop_reason"], "page_limit")
        self.assertFalse(result["complete"])

    def test_missing_list_with_positive_total_is_error(self):
        from ba_jobsuche.search import SearchError

        with self.assertRaises(SearchError):
            search(lambda _: {"maxErgebnisse": 2}, {})

    def test_empty_page_before_total_is_incomplete(self):
        result = search(lambda _: {"maxErgebnisse": 20, "ergebnisliste": []}, {}, 10, 3)
        self.assertFalse(result["complete"])
        self.assertEqual(result["stop_reason"], "unexpected_empty_page")

    def test_invalid_page_responses(self):
        from ba_jobsuche.search import SearchError

        cases = [
            None,
            {},
            {"maxErgebnisse": None},
            {"maxErgebnisse": "bad"},
            {"maxErgebnisse": -1},
            {"maxErgebnisse": 1, "ergebnisliste": None},
            {"maxErgebnisse": 1, "ergebnisliste": [None]},
            {"maxErgebnisse": 1, "ergebnisliste": [{}]},
            {"maxErgebnisse": 1, "ergebnisliste": [{"referenznummer": ""}]},
        ]
        for case in cases:
            with self.subTest(case=case), self.assertRaises(SearchError):
                search(lambda _, response=case: response, {})

    def test_invalid_limits(self):
        for size, pages in [(0, 1), (101, 1), (1, 0), (1, 101)]:
            with self.subTest(size=size, pages=pages), self.assertRaises(ValueError):
                search(lambda _: {}, {}, size, pages)

    def test_empty_zero_result(self):
        result = search(lambda _: {"maxErgebnisse": 0}, {})
        self.assertEqual(result["results"], [])
        self.assertTrue(result["complete"])
