import logging

from flask import Blueprint, current_app, jsonify, request

from notes.validation import clean_note, validate_note

api = Blueprint("api", __name__)
log = logging.getLogger("notes")


def store():
    return current_app.config["STORE"]


def error(status, *messages):
    return jsonify({"errors": list(messages)}), status


def note_from_request():
    data = request.get_json(silent=True)
    if data is None:
        return None, error(400, "request body must be JSON")
    problems = validate_note(data)
    if problems:
        return None, error(400, *problems)
    return clean_note(data), None


def page_args():
    try:
        limit = int(request.args.get("limit", current_app.config["PAGE_SIZE"]))
        offset = int(request.args.get("offset", 0))
    except ValueError:
        return None, error(400, "limit and offset must be whole numbers")
    if not 1 <= limit <= 500 or offset < 0:
        return None, error(400, "limit must be 1 to 500 and offset 0 or more")
    return (limit, offset), None


@api.get("/health")
def health():
    return jsonify({"status": "ok", "notes": store().count()})


@api.get("/notes")
def list_notes():
    page, err = page_args()
    if err:
        return err
    limit, offset = page
    found = store().list(
        query=request.args.get("q", "").strip(),
        tag=request.args.get("tag", "").strip().lower(),
        limit=limit,
        offset=offset,
    )
    return jsonify({"notes": found, "limit": limit, "offset": offset})


@api.post("/notes")
def create_note():
    fields, err = note_from_request()
    if err:
        return err
    note = store().add(**fields)
    log.info("created note %s", note["id"])
    return jsonify(note), 201


@api.get("/notes/<int:note_id>")
def get_note(note_id):
    note = store().get(note_id)
    return jsonify(note) if note else error(404, f"no note with id {note_id}")


@api.put("/notes/<int:note_id>")
def update_note(note_id):
    fields, err = note_from_request()
    if err:
        return err
    note = store().update(note_id, **fields)
    return jsonify(note) if note else error(404, f"no note with id {note_id}")


@api.delete("/notes/<int:note_id>")
def delete_note(note_id):
    if not store().delete(note_id):
        return error(404, f"no note with id {note_id}")
    log.info("deleted note %s", note_id)
    return "", 204
