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
