from flask import Flask, jsonify, request

from storage import NoteStore
from validation import validate_note


def error(status, *messages):
    return jsonify({"errors": list(messages)}), status


def read_note_json():
    """The validated note from the request, or an error response."""
    data = request.get_json(silent=True)
    if data is None:
        return None, error(400, "request body must be JSON")
    problems = validate_note(data)
    if problems:
        return None, error(400, *problems)
    return {"title": data["title"].strip(), "body": data.get("body", "")}, None


def create_app(db_path="notes.db"):
    app = Flask(__name__)
    store = NoteStore(db_path)

    @app.get("/notes")
    def list_notes():
        query = request.args.get("q", "").strip()
        return jsonify(store.search(query) if query else store.all())

    @app.post("/notes")
    def create_note():
        fields, err = read_note_json()
        if err:
            return err
        return jsonify(store.add(**fields)), 201

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
        return "", 204

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=8000, debug=True)
