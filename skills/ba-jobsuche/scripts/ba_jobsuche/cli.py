"""JSON command line interface for job research."""

import argparse
import json
from datetime import datetime, timezone
from typing import Any, NoReturn

from .api import ApiError, fetch_detail, fetch_search
from .search import DEFAULT_MAX_PAGES, DEFAULT_PAGE_SIZE, SearchError, search


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise ValueError(message)


def search_command(args: argparse.Namespace) -> dict[str, Any]:
    if not args.was.strip() or (args.wo is not None and not args.wo.strip()):
        raise ValueError("Search text and location must not be empty")
    query = {"was": args.was}
    if args.wo:
        query["wo"] = args.wo
    if args.homeoffice:
        query["homeoffice"] = f"prozentual_{args.homeoffice[:-1]}"
    return {"query": query, **search(fetch_search, query, args.size, args.max_pages)}


def detail_command(args: argparse.Namespace) -> dict[str, Any]:
    if not args.reference.strip():
        raise ValueError("Reference must not be empty")
    result = fetch_detail(args.reference)
    if not isinstance(result, dict):
        raise SearchError("Invalid detail response")
    return {"reference": args.reference, "result": result}


def dispatch(args: argparse.Namespace) -> dict[str, Any]:
    if args.command == "search":
        return search_command(args)
    if args.command == "detail":
        return detail_command(args)
    raise ValueError("Unsupported command")


def main(argv: list[str] | None = None) -> int:
    parser = Parser(description="Search BA Jobsuche")
    sub = parser.add_subparsers(dest="command", required=True)
    find = sub.add_parser("search", help="Search job offers")
    find.add_argument("--was", required=True, help="Search terms (required)")
    find.add_argument("--wo", help="Location; omit for no location filter")
    find.add_argument(
        "--homeoffice",
        nargs="?",
        const="100%",
        choices=("0%", "25%", "50%", "100%"),
        help="Home office filter: 0%%, 25%%, 50%%, 100%% (default: 100%%)",
    )
    find.add_argument(
        "--size",
        type=int,
        default=DEFAULT_PAGE_SIZE,
        help="Results per page, 1-100 (default: 100)",
    )
    find.add_argument(
        "--max-pages",
        type=int,
        default=DEFAULT_MAX_PAGES,
        help="Maximum pages to fetch, 1-100 (default: 10)",
    )
    detail = sub.add_parser("detail", help="Fetch a job offer by reference number")
    detail.add_argument("reference", help="Job offer reference number")
    try:
        args = parser.parse_args(argv)
        now = datetime.now(timezone.utc).isoformat()
        base = {
            "schema_version": 1,
            "ok": True,
            "source": "https://www.arbeitsagentur.de/jobsuche/",
            "retrieved_at": now,
        }
        data = {**base, **dispatch(args)}
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
