from dataclasses import dataclass


@dataclass(frozen=True)
class CheckResult:
    name: str
    type: str
    status: str
    response_time_ms: float
    message: str
