# SQLite storage

Notes now go into a SQLite file (`notes.db` next to the app) and survive a restart. `storage.py` wraps the three queries we need, `app.py` only talks to that class, and `validation.py` is unchanged from folder 04.

The app is built by `create_app(db_path)` now, so each test gets its own database in a temporary folder.

Run with `python3 app.py`. Tests: `python3 -m pytest`.
