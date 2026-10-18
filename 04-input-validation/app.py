from flask import Flask, jsonify, request

from validation import validate_note

app = Flask(__name__)

notes = {}
next_id = 1


@app.get("/notes")
def list_notes():
    return jsonify(list(notes.values()))


@app.post("/notes")
def create_note():
    global next_id
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"errors": ["request body must be JSON"]}), 400
    problems = validate_note(data)
    if problems:
        return jsonify({"errors": problems}), 400

    note = {"id": next_id, "title": data["title"].strip(), "body": data.get("body", "")}
    notes[next_id] = note
    next_id += 1
    return jsonify(note), 201


@app.get("/notes/<int:note_id>")
def get_note(note_id):
    note = notes.get(note_id)
    if note is None:
        return jsonify({"errors": [f"no note with id {note_id}"]}), 404
    return jsonify(note)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
