import logging
import sys
import time

from flask import Flask, g, jsonify, request
from werkzeug.exceptions import HTTPException

from config import Config, from_env
from storage import NoteStore
from validation import validate_note

log = logging.getLogger("notes")


def error(status, *messages):
    return jsonify({"errors": list(messages)}), status


def read_note_json():
    data = request.get_json(silent=True)
    if data is None:
        return None, error(400, "request body must be JSON")
    problems = validate_note(data)
    if problems:
        return None, error(400, *problems)
    return {"title": data["title"].strip(), "body": data.get("body", "")}, None


def create_app(config=None):
    config = config or Config()
    app = Flask(__name__)
    store = NoteStore(config.db_path)
    log.info("using database %s", config.db_path)

    @app.before_request
    def start_timer():
        g.started = time.perf_counter()

    @app.after_request
    def log_request(response):
        ms = (time.perf_counter() - g.started) * 1000
        log.info(
            "%s %s %s %.1fms", request.method, request.path, response.status_code, ms
        )
        return response

    @app.errorhandler(HTTPException)
    def http_error(e):
        # unknown routes, wrong methods and so on, all as JSON
        return error(e.code, e.description)

    @app.errorhandler(Exception)
    def unexpected_error(e):
        log.exception("unhandled error on %s %s", request.method, request.path)
        return error(500, "internal error")

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "notes": len(store.all())})

    @app.get("/notes")
    def list_notes():
        query = request.args.get("q", "").strip()
        return jsonify(store.search(query) if query else store.all())

    @app.post("/notes")
    def create_note():
        fields, err = read_note_json()
        if err:
            return err
        note = store.add(**fields)
        log.info("created note %s", note["id"])
        return jsonify(note), 201

    @app.get("/notes/<int:note_id>")
    def get_note(note_id):
        note = store.get(note_id)
        return jsonify(note) if note else error(404, f"no note with id {note_id}")

    @app.put("/notes/<int:note_id>")
    def update_note(note_id):
        fields, err = read_note_json()
        if err:
            return err
        note = store.update(note_id, **fields)
        return jsonify(note) if note else error(404, f"no note with id {note_id}")

    @app.delete("/notes/<int:note_id>")
    def delete_note(note_id):
        if not store.delete(note_id):
            return error(404, f"no note with id {note_id}")
        log.info("deleted note %s", note_id)
        return "", 204

    return app


def main():
    try:
        config = from_env()
    except ValueError as e:
        print(f"bad configuration: {e}", file=sys.stderr)
        sys.exit(2)
    logging.basicConfig(
        level=config.log_level, format="%(asctime)s %(levelname)s %(message)s"
    )
    create_app(config).run(host=config.host, port=config.port)


if __name__ == "__main__":
    main()
