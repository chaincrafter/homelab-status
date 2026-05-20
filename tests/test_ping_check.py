import subprocess

import homelab_status.checks.ping_check as ping_check


def test_ping_check_reports_up_when_ping_succeeds(monkeypatch):
    def fake_run(*args, **kwargs):
        return subprocess.CompletedProcess(args=args, returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(ping_check.subprocess, "run", fake_run)

    result = ping_check.check_ping({"name": "NAS", "type": "ping", "host": "192.168.1.2"})

    assert result.status == "up"
    assert result.message == "Ping succeeded for 192.168.1.2"


def test_ping_check_handles_missing_output_on_failure(monkeypatch):
    def fake_run(*args, **kwargs):
        return subprocess.CompletedProcess(args=args, returncode=1, stdout=None, stderr=None)

    monkeypatch.setattr(ping_check.subprocess, "run", fake_run)

    result = ping_check.check_ping({"name": "NAS", "type": "ping", "host": "192.168.1.2"})

    assert result.status == "down"
    assert result.message == "Ping failed for 192.168.1.2"
