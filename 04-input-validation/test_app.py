import pytest

import app as notes_app
from validation import validate_note


@pytest.fixture
def client():
    notes_app.notes.clear()
    notes_app.next_id = 1
    return notes_app.app.test_client()


def test_validate_good_note():
    assert validate_note({"title": "x", "body": "y"}) == []
    assert validate_note({"title": "x"}) == []


def test_validate_bad_notes():
    assert validate_note({"body": "y"}) == ["title is required"]
    assert validate_note({"title": "   "}) == ["title is required"]
    assert validate_note({"title": "a" * 101}) == [
        "title is longer than 100 characters"
    ]
    assert validate_note({"title": "x", "body": 5}) == ["body must be a string"]
    assert validate_note({"title": "x", "colour": "red"}) == ["unknown fields: colour"]
    assert validate_note([1, 2]) == ["body must be a JSON object"]


def test_create_strips_title(client):
    resp = client.post("/notes", json={"title": "  hello  "})
    assert resp.status_code == 201
    assert resp.get_json()["title"] == "hello"


def test_create_rejects_bad_input(client):
    resp = client.post("/notes", json={"body": "no title", "extra": 1})
    assert resp.status_code == 400
    assert resp.get_json()["errors"] == ["title is required", "unknown fields: extra"]
    assert client.get("/notes").get_json() == []


def test_create_rejects_non_json(client):
    resp = client.post("/notes", data="title=hi")
    assert resp.status_code == 400
    assert resp.get_json()["errors"] == ["request body must be JSON"]


def test_missing_note_has_json_error(client):
    resp = client.get("/notes/7")
    assert resp.status_code == 404
    assert resp.get_json() == {"errors": ["no note with id 7"]}
