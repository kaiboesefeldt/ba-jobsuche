"""Collect paginated search results without assigning ratings."""

DEFAULT_MAX_PAGES = 10
DEFAULT_PAGE_SIZE = 100


class SearchError(Exception):
    """The service response cannot be interpreted reliably."""


def search(fetch, query, page_size=DEFAULT_PAGE_SIZE, max_pages=DEFAULT_MAX_PAGES):
    if not 1 <= page_size <= 100 or not 1 <= max_pages <= 100:
        raise ValueError("Page size and page limit must be between 1 and 100")
    results, seen = [], set()
    totals = []
    for page in range(1, max_pages + 1):
        data = fetch({**query, "page": page, "size": page_size})
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
        totals.append(total)
        for entry in entries:
            if (
                not isinstance(entry, dict)
                or not isinstance(entry.get("referenznummer"), str)
                or not entry["referenznummer"]
            ):
                raise SearchError("Result is missing a reference number")
            if entry["referenznummer"] not in seen:
                seen.add(entry["referenznummer"])
                results.append(entry)
        if not entries and (page - 1) * page_size < total:
            reason = "unexpected_empty_page"
            break
        if not entries or page * page_size >= total:
            reason = "exhausted"
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
