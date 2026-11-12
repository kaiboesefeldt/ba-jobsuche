"""JSON command line interface for job research."""

import argparse
import json
from datetime import datetime, timezone
from itertools import product
from typing import Any, NoReturn

from .api import ApiError, fetch_detail, fetch_search
from .search import (
    DEFAULT_MAX_PAGES,
    DEFAULT_PAGE_SIZE,
    SearchError,
    add_unique,
    search,
)


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise ValueError(message)


def parse_location(value: str) -> dict[str, str | int]:
    if ":" not in value:
        return {"wo": value}
    location, radius = value.split(":", 1)
    if not location.strip() or not radius.isascii() or not radius.isdecimal():
        raise ValueError("Location radius must be a whole number from 0 to 200 km")
    radius = radius.lstrip("0") or "0"
    if len(radius) > 3 or int(radius) > 200:
        raise ValueError("Location radius must be a whole number from 0 to 200 km")
    return {"wo": location, "umkreis": int(radius)}


def display_values(values: list[str]) -> str:
    return values[0] if len(values) == 1 else json.dumps(values, ensure_ascii=False)


def search_queries(
    args: argparse.Namespace,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    locations = args.wo or []
    if any(not value.strip() for value in [*args.was, *locations]):
        raise ValueError("Search text and location must not be empty")
    parsed_locations = [parse_location(value) for value in locations] or [{}]
    query: dict[str, Any] = {"was": display_values(args.was)}
    if len(locations) == 1:
        query.update(parsed_locations[0])
    elif locations:
        query["wo"] = display_values(locations)
    common = {}
    if args.homeoffice:
        query["homeoffice"] = args.homeoffice
        common["homeoffice"] = f"prozentual_{args.homeoffice[:-1]}"
    queries = [
        {"was": term, **location, **common}
        for term, location in product(args.was, parsed_locations)
    ]
    return query, queries


def search_command(args: argparse.Namespace) -> dict[str, Any]:
    query, queries = search_queries(args)
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    pages = 0
    totals: list[int] = []
    reasons = {"exhausted": 0, "page_limit": 1, "unexpected_empty_page": 2}
    reason = "exhausted"
    for api_query in queries:
        part = search(fetch_search, api_query, args.size, args.max_pages)
        add_unique(part["results"], results, seen)
        pages += part["pages_fetched"]
        totals.extend(part["reported_totals"])
        reason = max((reason, part["stop_reason"]), key=reasons.__getitem__)
    return {
        "query": query,
        "results": results,
        "pages_fetched": pages,
        "reported_totals": totals,
        "stop_reason": reason,
        "complete": reason == "exhausted",
    }


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
    find.add_argument(
        "--was",
        required=True,
        action="append",
        help="Search terms (required; repeatable)",
    )
    find.add_argument(
        "--wo",
        action="append",
        help="Location or location:radius in km (0-200); omit for no location filter",
    )
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
