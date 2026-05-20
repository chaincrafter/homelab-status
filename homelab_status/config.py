from pathlib import Path
from typing import Any

import yaml


SUPPORTED_TYPES = {"http", "tcp", "ping"}
REQUIRED_FIELDS = {
    "http": {"name", "type", "url"},
    "tcp": {"name", "type", "host", "port"},
    "ping": {"name", "type", "host"},
}


class ConfigError(ValueError):
    """Raised when the service configuration is invalid."""


def load_config(path: str | Path) -> list[dict[str, Any]]:
    config_path = Path(path)

    if not config_path.exists():
        raise ConfigError(f"Config file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    services = data.get("services")
    if not isinstance(services, list):
        raise ConfigError("Config must contain a 'services' list")

    for index, service in enumerate(services, start=1):
        validate_service(service, index)

    return services


def validate_service(service: Any, index: int) -> None:
    if not isinstance(service, dict):
        raise ConfigError(f"Service #{index} must be a mapping")

    service_type = service.get("type")
    if service_type not in SUPPORTED_TYPES:
        raise ConfigError(
            f"Service #{index} has unsupported type '{service_type}'. "
            f"Supported types: {', '.join(sorted(SUPPORTED_TYPES))}"
        )

    missing = REQUIRED_FIELDS[service_type] - service.keys()
    if missing:
        missing_fields = ", ".join(sorted(missing))
        raise ConfigError(f"Service #{index} is missing required field(s): {missing_fields}")

    timeout = service.get("timeout", 2)
    if not isinstance(timeout, (int, float)) or timeout <= 0:
        raise ConfigError(f"Service #{index} timeout must be a positive number")

    if service_type == "tcp":
        port = service.get("port")
        if not isinstance(port, int) or not 1 <= port <= 65535:
            raise ConfigError(f"Service #{index} port must be an integer from 1 to 65535")
