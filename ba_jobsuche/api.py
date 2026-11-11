"""Transport for the unofficial BA Jobsuche service."""

import base64
import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service"
PUBLIC_API_KEY = "jobboerse-jobsuche"


class ApiError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def request(path: str, params: dict[str, Any] | None = None) -> Any:
    url = BASE_URL + path
    if params:
        url += "?" + urlencode(params)
    req = Request(
        url,
        headers={
            "X-API-Key": os.environ.get("JOBSUCHE_API_KEY", PUBLIC_API_KEY),
            "Accept": "application/json",
        },
    )
    try:
        with urlopen(req, timeout=15) as response:
            return json.load(response)
    except HTTPError as exc:
        raise ApiError("http_error", f"Service returned HTTP {exc.code}") from exc
    except (URLError, TimeoutError, OSError) as exc:
        raise ApiError("network_error", "Service request failed") from exc
    except (ValueError, UnicodeError) as exc:
        raise ApiError("invalid_response", "Service returned invalid JSON") from exc


def fetch_search(params: dict[str, Any]) -> Any:
    return request("/pc/v6/jobs", params)


def fetch_detail(reference: str) -> Any:
    encoded = base64.b64encode(reference.encode("utf-8")).decode("ascii")
    return request("/pc/v4/jobdetails/" + quote(encoded, safe=""))
