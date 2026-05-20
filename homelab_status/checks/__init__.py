from typing import Any

from homelab_status.checks.http_check import check_http
from homelab_status.checks.ping_check import check_ping
from homelab_status.checks.tcp_check import check_tcp
from homelab_status.models import CheckResult


def run_check(service: dict[str, Any]) -> CheckResult:
    service_type = service["type"]

    if service_type == "http":
        return check_http(service)
    if service_type == "tcp":
        return check_tcp(service)
    if service_type == "ping":
        return check_ping(service)

    return CheckResult(
        name=service.get("name", "Unknown"),
        type=str(service_type),
        status="down",
        response_time_ms=0,
        message=f"Unsupported check type: {service_type}",
    )
