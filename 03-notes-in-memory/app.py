from flask import Flask, abort, jsonify, request

app = Flask(__name__)

# notes live in memory, restarting the server empties the list
notes = {}
next_id = 1


@app.get("/notes")
def list_notes():
    return jsonify(list(notes.values()))


@app.post("/notes")
def create_note():
    global next_id
    data = request.get_json(silent=True) or {}
    note = {"id": next_id, "title": data.get("title", ""), "body": data.get("body", "")}
    notes[next_id] = note
    next_id += 1
    return jsonify(note), 201


@app.get("/notes/<int:note_id>")
def get_note(note_id):
    if note_id not in notes:
        abort(404)
    return jsonify(notes[note_id])


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
