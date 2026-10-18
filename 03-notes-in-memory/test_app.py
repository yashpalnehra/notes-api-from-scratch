import pytest

import app as notes_app


@pytest.fixture
def client():
    notes_app.notes.clear()
    notes_app.next_id = 1
    return notes_app.app.test_client()


def test_empty_at_start(client):
    assert client.get("/notes").get_json() == []


def test_create_and_fetch(client):
    resp = client.post("/notes", json={"title": "shopping", "body": "eggs, milk"})
    assert resp.status_code == 201
    note = resp.get_json()
    assert note == {"id": 1, "title": "shopping", "body": "eggs, milk"}

    assert client.get("/notes/1").get_json() == note
    assert client.get("/notes").get_json() == [note]


def test_ids_increase(client):
    client.post("/notes", json={"title": "a"})
    client.post("/notes", json={"title": "b"})
    assert [n["id"] for n in client.get("/notes").get_json()] == [1, 2]


def test_missing_note_is_404(client):
    assert client.get("/notes/99").status_code == 404
