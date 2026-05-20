from urllib.error import HTTPError, URLError

import homelab_status.checks.http_check as http_check


class FakeResponse:
    def __init__(self, status_code):
        self.status_code = status_code

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def getcode(self):
        return self.status_code


def test_http_check_reports_up_for_2xx(monkeypatch):
    monkeypatch.setattr(http_check, "urlopen", lambda url, timeout: FakeResponse(200))

    result = http_check.check_http({"name": "Web", "type": "http", "url": "http://test"})

    assert result.status == "up"
    assert result.message == "HTTP 200"
    assert result.response_time_ms >= 0


def test_http_check_reports_degraded_for_4xx(monkeypatch):
    def fake_urlopen(url, timeout):
        raise HTTPError(url, 404, "Not Found", hdrs=None, fp=None)

    monkeypatch.setattr(http_check, "urlopen", fake_urlopen)

    result = http_check.check_http({"name": "Web", "type": "http", "url": "http://test"})

    assert result.status == "degraded"
    assert result.message == "HTTP 404"


def test_http_check_reports_down_for_5xx(monkeypatch):
    def fake_urlopen(url, timeout):
        raise HTTPError(url, 500, "Server Error", hdrs=None, fp=None)

    monkeypatch.setattr(http_check, "urlopen", fake_urlopen)

    result = http_check.check_http({"name": "Web", "type": "http", "url": "http://test"})

    assert result.status == "down"
    assert result.message == "HTTP 500"


def test_http_check_reports_down_for_connection_error(monkeypatch):
    def fake_urlopen(url, timeout):
        raise URLError("connection refused")

    monkeypatch.setattr(http_check, "urlopen", fake_urlopen)

    result = http_check.check_http({"name": "Web", "type": "http", "url": "http://test"})

    assert result.status == "down"
    assert "connection refused" in result.message
