import platform
import subprocess
from time import perf_counter
from typing import Any

from homelab_status.models import CheckResult


def check_ping(service: dict[str, Any]) -> CheckResult:
    name = service["name"]
    host = service["host"]
    timeout = service.get("timeout", 2)

    command = build_ping_command(host, timeout)
    start = perf_counter()

    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout + 1,
            check=False,
        )
    except (subprocess.TimeoutExpired, OSError) as error:
        return CheckResult(name, "ping", "down", elapsed_ms(start), str(error))

    response_time = elapsed_ms(start)
    if completed.returncode == 0:
        return CheckResult(name, "ping", "up", response_time, f"Ping succeeded for {host}")

    stdout = completed.stdout or ""
    stderr = completed.stderr or ""
    message = stderr.strip() or stdout.strip() or f"Ping failed for {host}"
    return CheckResult(name, "ping", "down", response_time, message)


def build_ping_command(host: str, timeout: int | float) -> list[str]:
    if platform.system().lower() == "windows":
        timeout_ms = max(1, int(timeout * 1000))
        return ["ping", "-n", "1", "-w", str(timeout_ms), host]

    timeout_seconds = max(1, int(round(timeout)))
    return ["ping", "-c", "1", "-W", str(timeout_seconds), host]


def elapsed_ms(start: float) -> float:
    return round((perf_counter() - start) * 1000, 2)
