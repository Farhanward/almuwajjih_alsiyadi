"""Almuwajjih Alsiyadi router as a local HTTP service.

``POST /api/route`` accepts ``{"prompt", "sensitivity", "budget_usd",
"max_latency_ms", "coding"}`` and returns the routing target
(``local`` / ``local_fast`` / ``cloud_coder``) with an Arabic reason.
Invariant: sensitive prompts are never routed to the cloud.
"""

from __future__ import annotations

from http.server import ThreadingHTTPServer
from typing import Any

from .http_base import BaseServiceHandler, build_server
from .router import route_request


def _route_route(data: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    prompt = str(data.get("prompt") or "").strip()
    if not prompt:
        return 400, {"ok": False, "error": "missing 'prompt'"}
    return 200, {"ok": True, **route_request(data)}


class Handler(BaseServiceHandler):
    post_routes = {"/api/route": staticmethod(_route_route)}


def create_server(host: str | None = None, port: int | None = None) -> ThreadingHTTPServer:
    return build_server(Handler, host=host, port=port)


def run_server(host: str | None = None, port: int | None = None) -> None:
    from .version import __version__

    server = create_server(host=host, port=port)
    print(f"almuwajjih service v{__version__}: http://{server.server_address[0]}:{server.server_address[1]}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
