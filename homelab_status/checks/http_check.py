from time import perf_counter
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from homelab_status.models import CheckResult


def check_http(service: dict[str, Any]) -> CheckResult:
    name = service["name"]
    url = service["url"]
    timeout = service.get("timeout", 2)

    start = perf_counter()
    try:
        with urlopen(url, timeout=timeout) as response:
            status_code = response.getcode()
            response_time = elapsed_ms(start)

        if 200 <= status_code <= 399:
            return CheckResult(name, "http", "up", response_time, f"HTTP {status_code}")
        if 400 <= status_code <= 499:
            return CheckResult(name, "http", "degraded", response_time, f"HTTP {status_code}")

        return CheckResult(name, "http", "down", response_time, f"HTTP {status_code}")

    except HTTPError as error:
        response_time = elapsed_ms(start)
        if 400 <= error.code <= 499:
            return CheckResult(name, "http", "degraded", response_time, f"HTTP {error.code}")
        return CheckResult(name, "http", "down", response_time, f"HTTP {error.code}")
    except (TimeoutError, URLError, OSError) as error:
        return CheckResult(name, "http", "down", elapsed_ms(start), str(error))


def elapsed_ms(start: float) -> float:
    return round((perf_counter() - start) * 1000, 2)
