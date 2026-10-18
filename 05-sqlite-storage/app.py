from flask import Flask, jsonify, request

from storage import NoteStore
from validation import validate_note


def create_app(db_path="notes.db"):
    app = Flask(__name__)
    store = NoteStore(db_path)

    @app.get("/notes")
    def list_notes():
        return jsonify(store.all())

    @app.post("/notes")
    def create_note():
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"errors": ["request body must be JSON"]}), 400
        problems = validate_note(data)
        if problems:
            return jsonify({"errors": problems}), 400
        note = store.add(data["title"].strip(), data.get("body", ""))
        return jsonify(note), 201

    @app.get("/notes/<int:note_id>")
    def get_note(note_id):
        note = store.get(note_id)
        if note is None:
            return jsonify({"errors": [f"no note with id {note_id}"]}), 404
        return jsonify(note)

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=8000, debug=True)
