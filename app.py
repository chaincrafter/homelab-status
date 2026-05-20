from dataclasses import asdict
from pathlib import Path

from flask import Flask, jsonify, render_template

from homelab_status.checks import run_check
from homelab_status.config import load_config


app = Flask(__name__)


def config_path() -> Path:
    local_config = Path("config.yaml")
    if local_config.exists():
        return local_config
    return Path("config.example.yaml")


def get_status_results():
    services = load_config(config_path())
    return [run_check(service) for service in services]


@app.route("/")
def dashboard():
    results = get_status_results()
    return render_template("dashboard.html", results=results)


@app.route("/api/status")
def api_status():
    results = get_status_results()
    return jsonify([asdict(result) for result in results])


if __name__ == "__main__":
    app.run(debug=True)
