"""Bounded, observational comparison of the undocumented BA publication options."""

import json
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parents[1] / "skills/ba-jobsuche/scripts")
)

from ba_jobsuche.api import fetch_search
from ba_jobsuche.search import publication_date, search


def main():
    base = {
        "was": "Softwareentwickler",
        "wo": "Berlin",
        "umkreis": 50,
        "sort": "veroeffdatum",
    }
    today = date.today()
    raw = search(fetch_search, base, 100, 3)
    filtered = search(fetch_search, {**base, "veroeffentlichtseit": 7}, 100, 3)
    cutoff = today - timedelta(days=7)
    local = {
        entry["referenznummer"]
        for entry in raw["results"]
        if (day := publication_date(entry)) is not None and day >= cutoff
    }
    api = {entry["referenznummer"] for entry in filtered["results"]}
    dates = [publication_date(entry) for entry in raw["results"]]
    known = [day for day in dates if day is not None]
    print(
        json.dumps(
            {
                "pages_unfiltered": raw["pages_fetched"],
                "complete_unfiltered": raw["complete"],
                "pages_filtered": filtered["pages_fetched"],
                "complete_filtered": filtered["complete"],
                "local_count": len(local),
                "api_count": len(api),
                "local_missing_from_api": len(local - api),
                "api_extra": len(api - local),
                "unknown_unfiltered": len(dates) - len(known),
                "known_dates_descending": known == sorted(known, reverse=True),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
