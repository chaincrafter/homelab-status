import socket
from time import perf_counter
from typing import Any

from homelab_status.models import CheckResult


def check_tcp(service: dict[str, Any]) -> CheckResult:
    name = service["name"]
    host = service["host"]
    port = service["port"]
    timeout = service.get("timeout", 2)

    start = perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            response_time = elapsed_ms(start)
        return CheckResult(name, "tcp", "up", response_time, f"Connected to {host}:{port}")
    except (TimeoutError, OSError) as error:
        return CheckResult(name, "tcp", "down", elapsed_ms(start), str(error))


def elapsed_ms(start: float) -> float:
    return round((perf_counter() - start) * 1000, 2)
