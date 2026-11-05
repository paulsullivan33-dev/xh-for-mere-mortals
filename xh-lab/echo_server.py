#!/usr/bin/env python3
"""echo_server.py — the xh guide's fixture HTTP server.

Binds 127.0.0.1:18092 and answers every request with a JSON
report of exactly what arrived: the method, the path, the
query string (raw and parsed), the headers in the order they
were received, and the body — parsed as JSON, as a form, or
as multipart uploads when the content type says so, and
shown raw otherwise. Because the server reports the request
back, every claim the guide makes about what xh sent can be
checked against the server's own words.

Special paths:
  /status/201   the echo report, with a 201 status
  /status/404   a small JSON error body, with a 404 status
  /status/500   a small JSON error body, with a 500 status
  /redirect     a 302 whose Location is /echo?via=redirect
  /download     a plain-text attachment, packing-list.txt
Every other path gets the echo report with a 200 status.

Each request is also appended as one line to the log file
named by XH_LAB_LOG (default: server-requests.log beside
this script), so a chapter can prove a request did *not*
arrive by counting lines before and after.

Standard library only. Run it in the background:
  python3 echo_server.py &
"""

import hashlib
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.environ.get("XH_LAB_LOG", os.path.join(HERE, "server-requests.log"))
PORT = 18092


def parse_multipart(body, boundary):
    """Split a multipart/form-data body into its parts.

    Just enough parsing for the lab's own client: returns a
    list of dicts with each part's field name, filename and
    content type (when present), size, sha256, and a short
    text preview when the part is small and textual.
    """
    parts = []
    delimiter = b"--" + boundary.encode()
    for chunk in body.split(delimiter):
        if chunk.startswith(b"--"):  # the closing delimiter
            break
        if chunk.startswith(b"\r\n"):
            chunk = chunk[2:]
        if chunk.endswith(b"\r\n"):  # the framing CRLF, exactly one
            chunk = chunk[:-2]
        if not chunk:
            continue
        head, _, data = chunk.partition(b"\r\n\r\n")
        part = {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}
        for line in head.decode("utf-8", "replace").split("\r\n"):
            if line.lower().startswith("content-disposition:"):
                for piece in line.split(";"):
                    piece = piece.strip()
                    if piece.startswith("name="):
                        part["name"] = piece[5:].strip('"')
                    elif piece.startswith("filename="):
                        part["filename"] = piece[9:].strip('"')
            elif line.lower().startswith("content-type:"):
                part["content_type"] = line.split(":", 1)[1].strip()
        try:
            text = data.decode("utf-8")
            if len(text) <= 200:
                part["text"] = text
        except UnicodeDecodeError:
            pass
        parts.append(part)
    return parts


class EchoHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):  # keep the console quiet
        pass

    def _report(self, status=200, extra=None):
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else b""
        split = urlsplit(self.path)
        ctype = self.headers.get("Content-Type", "")
        report = {
            "method": self.command,
            "path": split.path,
            "query_string": split.query,
            "query": parse_qs(split.query),
            "headers": [[k, v] for k, v in self.headers.items()],
            "content_type": ctype,
            "body_length": len(body),
        }
        if extra:
            report.update(extra)
        if ctype.startswith("application/json") and body:
            try:
                report["json"] = json.loads(body)
            except ValueError:
                report["body_text"] = body.decode("utf-8", "replace")
        elif ctype.startswith("application/x-www-form-urlencoded"):
            report["form"] = parse_qs(body.decode("utf-8", "replace"))
        elif ctype.startswith("multipart/form-data"):
            boundary = ctype.split("boundary=", 1)[1]
            report["multipart"] = parse_multipart(body, boundary)
        elif body:
            try:
                report["body_text"] = body.decode("utf-8")
            except UnicodeDecodeError:
                report["body_sha256"] = hashlib.sha256(body).hexdigest()
        self._send_json(status, report)

    def _send_json(self, status, obj):
        payload = json.dumps(obj, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(payload)

    def _handle(self):
        with open(LOG, "a") as fh:
            fh.write(f"{self.command} {self.path}\n")
        path = urlsplit(self.path).path
        if path == "/compact":
            self._drain()
            payload = (b'{"order":"bench-12","items":'
                       b'[{"name":"claw hammer","qty":2},'
                       b'{"name":"tape measure","qty":1}],'
                       b'"gift":false}')
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(payload)
        elif path == "/status/404":
            self._drain()
            self._send_json(404, {"error": "no such workshop order",
                                  "path": path})
        elif path == "/status/500":
            self._drain()
            self._send_json(500, {"error": "the stores lift is stuck",
                                  "path": path})
        elif path == "/status/201":
            self._report(status=201)
        elif path == "/redirect":
            self._drain()
            self.send_response(302)
            self.send_header("Location", "/echo?via=redirect")
            self.send_header("Content-Length", "0")
            self.end_headers()
        elif path == "/download":
            self._drain()
            payload = (b"Packing list - bench order 12\n"
                       b"2x claw hammer\n1x tape measure\n"
                       b"4x wall plugs, 6 mm\n")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header(
                "Content-Disposition",
                'attachment; filename="packing-list.txt"')
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(payload)
        else:
            self._report()

    def _drain(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length:
            self.rfile.read(length)

    do_GET = _handle
    do_POST = _handle
    do_PUT = _handle
    do_PATCH = _handle
    do_DELETE = _handle
    do_HEAD = _handle
    do_OPTIONS = _handle


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", PORT), EchoHandler)
    print(f"echo server on http://127.0.0.1:{PORT}", file=sys.stderr)
    server.serve_forever()
