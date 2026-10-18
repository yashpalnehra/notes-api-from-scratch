import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "127.0.0.1"
PORT = 8000


def health():
    return 200, {"status": "ok"}


def now():
    return 200, {"utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}


ROUTES = {"/health": health, "/time": now}


class JsonHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        handler = ROUTES.get(self.path)
        if handler is None:
            self.send_json(404, {"error": f"no route for {self.path}"})
            return
        status, payload = handler()
        self.send_json(status, payload)

    def send_json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # one short line per request instead of the default verbose log
        print(f"{self.command} {self.path}")


def make_server(host=HOST, port=PORT):
    return HTTPServer((host, port), JsonHandler)


if __name__ == "__main__":
    server = make_server()
    print(f"listening on http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
