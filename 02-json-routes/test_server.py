import json
import threading
import urllib.error
import urllib.request

import pytest

from server import make_server


@pytest.fixture(scope="module")
def base_url():
    # port 0 lets the OS pick a free one
    server = make_server("127.0.0.1", 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_address[1]}"
    server.shutdown()


def get(url):
    try:
        with urllib.request.urlopen(url) as resp:
            return resp.status, json.load(resp)
    except urllib.error.HTTPError as e:
        return e.code, json.load(e)


def test_health(base_url):
    assert get(base_url + "/health") == (200, {"status": "ok"})


def test_time_has_utc_field(base_url):
    status, body = get(base_url + "/time")
    assert status == 200
    assert body["utc"].endswith("+00:00")


def test_unknown_route_is_json_404(base_url):
    status, body = get(base_url + "/nope")
    assert status == 404
    assert "no route" in body["error"]
