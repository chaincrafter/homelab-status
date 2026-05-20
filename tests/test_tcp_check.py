import socket

import homelab_status.checks.tcp_check as tcp_check


class FakeSocket:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False


def test_tcp_check_reports_up_when_connection_succeeds(monkeypatch):
    monkeypatch.setattr(
        tcp_check.socket,
        "create_connection",
        lambda address, timeout: FakeSocket(),
    )

    result = tcp_check.check_tcp(
        {"name": "Router", "type": "tcp", "host": "192.168.1.1", "port": 80}
    )

    assert result.status == "up"
    assert result.message == "Connected to 192.168.1.1:80"
    assert result.response_time_ms >= 0


def test_tcp_check_reports_down_when_connection_fails(monkeypatch):
    def fake_create_connection(address, timeout):
        raise socket.timeout("timed out")

    monkeypatch.setattr(tcp_check.socket, "create_connection", fake_create_connection)

    result = tcp_check.check_tcp(
        {"name": "Router", "type": "tcp", "host": "192.168.1.1", "port": 80}
    )

    assert result.status == "down"
    assert "timed out" in result.message
