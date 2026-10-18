# Notes in memory

First Flask app. Notes are kept in a dict, so they vanish when the server stops.

    GET  /notes          all notes
    POST /notes          create one from {"title": ..., "body": ...}
    GET  /notes/<id>     one note, or 404

Install the pinned packages from the repo root first (`pip install -r requirements.txt`), then `python3 app.py`. Try it:

    curl -X POST http://127.0.0.1:8000/notes -H 'Content-Type: application/json' -d '{"title": "hi", "body": "first note"}'
    curl http://127.0.0.1:8000/notes

Tests use Flask's test client, no server needed: `python3 -m pytest`.
