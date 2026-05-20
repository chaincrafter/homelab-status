# homelab-status

`homelab-status` is a lightweight self-hosted dashboard for checking the availability of local homelab services.

It monitors configured services such as Home Assistant, NAS systems, routers, access points, local APIs, web services and development machines using simple HTTP, TCP and ping checks.

The goal is not to replace full monitoring stacks like Prometheus, Grafana or Uptime Kuma. Instead, this project provides a small, understandable and easily extensible status page for local infrastructure.

## Use case

Run `homelab-status` on a local machine to get a quick status overview of important services in your home network.

## Features

- Simple YAML-based service configuration
- HTTP health checks
- TCP port checks
- Ping checks
- Response time measurement
- Clean web dashboard
- Service status overview: up, down or degraded
- Designed for local homelab environments
- Small codebase, easy to understand and extend

## Installation

```bash
python -m venv .venv
pip install -r requirements.txt
```

## Configuration

Copy the example configuration and adjust it for your network:

```bash
copy config.example.yaml config.yaml
```

On Linux or macOS:

```bash
cp config.example.yaml config.yaml
```

Example service configuration:

```yaml
services:
  - name: Home Assistant
    type: http
    url: http://192.168.30.10:8123
    timeout: 2

  - name: NAS
    type: ping
    host: 192.168.30.20
    timeout: 2

  - name: Router
    type: tcp
    host: 192.168.30.1
    port: 80
    timeout: 2
```

Supported check types:

- `http` requires `url`
- `tcp` requires `host` and `port`
- `ping` requires `host`

## Running locally

```bash
flask --app app run
```

Then open `http://127.0.0.1:5000`.

The JSON status endpoint is available at `http://127.0.0.1:5000/api/status`.

## Testing

```bash
pytest
```

## Example dashboard screenshot

Screenshot placeholder: add a dashboard screenshot here after the first UI capture.

## MVP scope

This project intentionally starts small.

The first version focuses on:

- reading services from a configuration file
- checking service availability
- displaying results in a web dashboard
- keeping the codebase simple and testable

Advanced monitoring, authentication, alerting and historical metrics are planned as later improvements.

## Roadmap

- SQLite-based status history
- Uptime percentage per service
- Docker support
- Prometheus exporter endpoint
- Basic authentication
- Dark mode
- Telegram or email alerts
- Configurable check intervals
- Service groups
- JSON API endpoint

## Portfolio purpose

This project demonstrates practical backend and DevOps skills:

- service health checking
- configuration-driven application design
- basic network diagnostics
- clean Python project structure
- testable architecture
- self-hosted tooling
- local infrastructure monitoring

It is built as a small but realistic portfolio project rather than a production-grade monitoring platform.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
