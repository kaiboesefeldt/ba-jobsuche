"""Collect paginated search results without assigning ratings."""

from collections.abc import Callable
from typing import Any

DEFAULT_MAX_PAGES = 10
DEFAULT_PAGE_SIZE = 100
MAX_PAGES = 100
MAX_PAGE_SIZE = 100


class SearchError(Exception):
    """The service response cannot be interpreted reliably."""


def parse_page(data: Any) -> tuple[int, list[dict[str, Any]]]:
    if not isinstance(data, dict):
        raise SearchError("Invalid search response")
    try:
        total = int(data["maxErgebnisse"])
    except (KeyError, TypeError, ValueError) as exc:
        raise SearchError("Missing or invalid result count") from exc
    if total < 0:
        raise SearchError("Invalid result count")
    entries = data.get("ergebnisliste", [] if total == 0 else None)
    if not isinstance(entries, list):
        raise SearchError("Missing or invalid result list")
    for entry in entries:
        if (
            not isinstance(entry, dict)
            or not isinstance(entry.get("referenznummer"), str)
            or not entry["referenznummer"]
        ):
            raise SearchError("Result is missing a reference number")
    return total, entries


def add_unique(
    entries: list[dict[str, Any]], results: list[dict[str, Any]], seen: set[str]
) -> None:
    for entry in entries:
        reference = entry["referenznummer"]
        if reference not in seen:
            seen.add(reference)
            results.append(entry)


def stop_reason(
    page: int, page_size: int, total: int, entries: list[dict[str, Any]]
) -> str | None:
    if not entries and (page - 1) * page_size < total:
        return "unexpected_empty_page"
    if not entries or page * page_size >= total:
        return "exhausted"
    return None


def search(
    fetch: Callable[[dict[str, Any]], Any],
    query: dict[str, Any],
    page_size: int = DEFAULT_PAGE_SIZE,
    max_pages: int = DEFAULT_MAX_PAGES,
) -> dict[str, Any]:
    if not 1 <= page_size <= MAX_PAGE_SIZE or not 1 <= max_pages <= MAX_PAGES:
        raise ValueError("Page size and page limit must be between 1 and 100")
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    totals: list[int] = []
    for page in range(1, max_pages + 1):
        total, entries = parse_page(fetch({**query, "page": page, "size": page_size}))
        totals.append(total)
        add_unique(entries, results, seen)
        reason = stop_reason(page, page_size, total, entries)
        if reason is not None:
            break
    else:
        reason = "page_limit"
    return {
        "results": results,
        "pages_fetched": page,
        "reported_totals": totals,
        "stop_reason": reason,
        "complete": reason == "exhausted",
    }
