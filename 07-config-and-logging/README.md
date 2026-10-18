# Config and logging

The routes are the same as folder 06. What changes is everything around them.

Settings come from environment variables with sensible defaults, so nothing is hard-coded in the app.

    NOTES_DB          path of the SQLite file, default notes.db
    NOTES_HOST        default 127.0.0.1
    NOTES_PORT        default 8000
    NOTES_LOG_LEVEL   default INFO

Every request is logged with its method, path, status and time taken. Any HTTP error, including an unknown route or a wrong method, comes back as `{"errors": [...]}`. An unexpected exception is logged with its traceback and the client gets a plain 500.

Run with `python3 app.py`, or for example `NOTES_PORT=9000 NOTES_LOG_LEVEL=DEBUG python3 app.py`. There's also a `/health` route for a quick check. Tests: `python3 -m pytest`.
