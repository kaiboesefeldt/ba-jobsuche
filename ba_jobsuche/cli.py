"""JSON command line interface for job research."""

import argparse
import json
from datetime import datetime, timezone

from .api import ApiError, fetch_detail, fetch_search
from .search import DEFAULT_MAX_PAGES, DEFAULT_PAGE_SIZE, SearchError, search


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


def main(argv=None):
    parser = Parser(description="Search BA Jobsuche")
    sub = parser.add_subparsers(dest="command", required=True)
    find = sub.add_parser("search")
    find.add_argument("--was", required=True)
    find.add_argument("--wo")
    find.add_argument(
        "--homeoffice", action="store_true", help="Filter for home or telework"
    )
    find.add_argument("--size", type=int, default=DEFAULT_PAGE_SIZE)
    find.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES)
    detail = sub.add_parser("detail")
    detail.add_argument("reference")
    try:
        args = parser.parse_args(argv)
        now = datetime.now(timezone.utc).isoformat()
        base = {
            "schema_version": 1,
            "ok": True,
            "source": "https://www.arbeitsagentur.de/jobsuche/",
            "retrieved_at": now,
        }
        if args.command == "search":
            if not args.was.strip() or (args.wo is not None and not args.wo.strip()):
                raise ValueError("Search text and location must not be empty")
            query = {"was": args.was}
            if args.wo:
                query["wo"] = args.wo
            if args.homeoffice:
                query["arbeitszeit"] = "ho"
            data = {
                **base,
                "query": query,
                **search(fetch_search, query, args.size, args.max_pages),
            }
        else:
            if not args.reference.strip():
                raise ValueError("Reference must not be empty")
            result = fetch_detail(args.reference)
            if not isinstance(result, dict):
                raise SearchError("Invalid detail response")
            data = {**base, "reference": args.reference, "result": result}
        status = 0
    except (ValueError, SearchError, ApiError) as exc:
        code = (
            exc.code
            if isinstance(exc, ApiError)
            else "invalid_response"
            if isinstance(exc, SearchError)
            else "invalid_input"
        )
        data = {
            "schema_version": 1,
            "ok": False,
            "error": {"code": code, "message": str(exc)},
        }
        status = 1
    print(json.dumps(data, ensure_ascii=False))
    return status
