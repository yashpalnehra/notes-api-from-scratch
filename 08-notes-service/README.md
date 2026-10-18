# Notes service

The finished version: a small notes API with tags, search, paging, SQLite storage, config from the environment, request logging and a test suite. Everything the earlier folders built up, arranged as a package.

    notes/__init__.py     create_app, logging and the error handlers
    notes/routes.py       the HTTP routes
    notes/storage.py      SQLite, two tables (notes and note_tags)
    notes/validation.py   what a valid note looks like
    notes/config.py       NOTES_* environment variables
    run.py                starts the server
    tests/                pytest suite, one temporary database per test

## How to run

From the repo root, `pip install -r requirements.txt` once. Then, in this folder:

    python3 run.py

It listens on 127.0.0.1:8000 and creates `notes.db` on first use. Set `NOTES_PORT`, `NOTES_DB`, `NOTES_LOG_LEVEL` or `NOTES_PAGE_SIZE` to change the defaults.

    curl -X POST localhost:8000/notes -H 'Content-Type: application/json' \
         -d '{"title": "Plan", "body": "write tests", "tags": ["work"]}'
    curl 'localhost:8000/notes?tag=work'
    curl 'localhost:8000/notes?q=tests&limit=10&offset=0'
    curl -X PUT localhost:8000/notes/1 -H 'Content-Type: application/json' -d '{"title": "Plan v2"}'
    curl -X DELETE localhost:8000/notes/1
    curl localhost:8000/health

Any error is JSON in the shape `{"errors": [...]}`. Tags are lowercased single words, at most ten per note.

## Tests

    python3 -m pytest

The `pyproject.toml` only tells pytest where the package and the tests are.
