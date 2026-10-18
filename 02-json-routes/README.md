# JSON routes

Still standard library only, but now with a small route table and JSON responses.

    GET /health     {"status": "ok"}
    GET /time       the current UTC time
    anything else   a 404, also as JSON

Run `python3 server.py` and try `curl http://127.0.0.1:8000/time`. The tests start the server on a random port in a thread, so `python3 -m pytest` works without anything running.
