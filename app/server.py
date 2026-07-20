#!/usr/bin/env python3
"""Local web UI + API for b23wrap lab demo."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core import generate  # noqa: E402


class Handler(BaseHTTPRequestHandler):
    server_version = "b23wrap/1.0"

    def log_message(self, fmt: str, *args) -> None:  # noqa: A003
        print(f"[{self.log_date_time_string()}] {args[0] if args else fmt}")

    def _cors(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, code: int, obj: dict) -> None:
        raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors()
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        path = urllib.parse.urlparse(self.path).path
        if path in ("/", "/index.html"):
            return self._file(STATIC / "index.html", "text/html; charset=utf-8")
        if path.startswith("/static/"):
            rel = path[len("/static/") :]
            fp = (STATIC / rel).resolve()
            if not str(fp).startswith(str(STATIC.resolve())) or not fp.is_file():
                return self._json(404, {"ok": False, "error": "not found"})
            ctype = {
                ".css": "text/css; charset=utf-8",
                ".js": "application/javascript; charset=utf-8",
            }.get(fp.suffix.lower(), "application/octet-stream")
            return self._file(fp, ctype)
        if path == "/api/health":
            return self._json(200, {"ok": True, "service": "b23wrap"})
        return self._json(404, {"ok": False, "error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        path = urllib.parse.urlparse(self.path).path
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return self._json(400, {"ok": False, "error": "JSON 无效"})

        if path != "/api/generate":
            return self._json(404, {"ok": False, "error": "not found"})

        try:
            result = generate(body.get("url") or body.get("target") or "")
            self._json(200, result)
        except ValueError as e:
            self._json(400, {"ok": False, "error": str(e)})
        except Exception as e:  # noqa: BLE001
            self._json(502, {"ok": False, "error": str(e)})

    def _file(self, fp: Path, content_type: str) -> None:
        data = fp.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self._cors()
        self.end_headers()
        self.wfile.write(data)


def main() -> None:
    ap = argparse.ArgumentParser(description="b23wrap local demo server")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()

    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"b23wrap: http://{args.host}:{args.port}/")
    print("Local research use only. Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")
        httpd.server_close()


if __name__ == "__main__":
    main()
