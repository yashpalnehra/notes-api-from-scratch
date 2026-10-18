import pytest

from app import create_app
from storage import NoteStore


@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "test.db")


@pytest.fixture
def client(db_path):
    return create_app(db_path).test_client()


def test_store_round_trip(db_path):
    store = NoteStore(db_path)
    note = store.add("first", "hello")
    assert note == {"id": 1, "title": "first", "body": "hello"}
    assert store.get(1) == note
    assert store.get(2) is None
    assert store.all() == [note]
    store.close()


def test_notes_survive_a_restart(db_path):
    client = create_app(db_path).test_client()
    client.post("/notes", json={"title": "keep me"})

    # a second app on the same file sees the note
    again = create_app(db_path).test_client()
    assert [n["title"] for n in again.get("/notes").get_json()] == ["keep me"]


def test_create_and_get(client):
    resp = client.post("/notes", json={"title": "t", "body": "b"})
    assert resp.status_code == 201
    note_id = resp.get_json()["id"]
    assert client.get(f"/notes/{note_id}").get_json() == {
        "id": note_id,
        "title": "t",
        "body": "b",
    }


def test_validation_still_applies(client):
    resp = client.post("/notes", json={})
    assert resp.status_code == 400
    assert resp.get_json()["errors"] == ["title is required"]
