import pytest

from homelab_status.config import ConfigError, load_config


def write_config(tmp_path, content):
    path = tmp_path / "config.yaml"
    path.write_text(content, encoding="utf-8")
    return path


def test_load_config_validates_services(tmp_path):
    path = write_config(
        tmp_path,
        """
services:
  - name: Web
    type: http
    url: http://example.test
  - name: Router
    type: tcp
    host: 192.168.1.1
    port: 80
  - name: NAS
    type: ping
    host: 192.168.1.2
""",
    )

    services = load_config(path)

    assert len(services) == 3
    assert services[0]["name"] == "Web"


def test_load_config_rejects_missing_required_field(tmp_path):
    path = write_config(
        tmp_path,
        """
services:
  - name: Broken HTTP
    type: http
""",
    )

    with pytest.raises(ConfigError, match="url"):
        load_config(path)


def test_load_config_rejects_unsupported_type(tmp_path):
    path = write_config(
        tmp_path,
        """
services:
  - name: Unknown
    type: dns
    host: example.test
""",
    )

    with pytest.raises(ConfigError, match="unsupported type"):
        load_config(path)


def test_load_config_rejects_invalid_tcp_port(tmp_path):
    path = write_config(
        tmp_path,
        """
services:
  - name: Router
    type: tcp
    host: 192.168.1.1
    port: 70000
""",
    )

    with pytest.raises(ConfigError, match="port"):
        load_config(path)
