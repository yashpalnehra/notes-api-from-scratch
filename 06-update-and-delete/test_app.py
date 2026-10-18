import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    return create_app(str(tmp_path / "test.db")).test_client()


def make(client, title, body=""):
    return client.post("/notes", json={"title": title, "body": body}).get_json()


def test_update(client):
    note = make(client, "old", "text")
    resp = client.put(f"/notes/{note['id']}", json={"title": "new", "body": "text"})
    assert resp.status_code == 200
    assert resp.get_json() == {"id": note["id"], "title": "new", "body": "text"}


def test_update_is_validated(client):
    note = make(client, "a")
    resp = client.put(f"/notes/{note['id']}", json={"body": "no title"})
    assert resp.status_code == 400
    assert client.get(f"/notes/{note['id']}").get_json()["title"] == "a"


def test_update_missing_note(client):
    assert client.put("/notes/42", json={"title": "x"}).status_code == 404


def test_delete(client):
    note = make(client, "bye")
    assert client.delete(f"/notes/{note['id']}").status_code == 204
    assert client.get(f"/notes/{note['id']}").status_code == 404
    assert client.delete(f"/notes/{note['id']}").status_code == 404


def test_search(client):
    make(client, "Shopping list", "eggs and milk")
    make(client, "Work", "call the plumber")
    make(client, "Ideas", "buy more EGGS")
    titles = lambda resp: [n["title"] for n in resp.get_json()]
    assert titles(client.get("/notes?q=eggs")) == ["Shopping list", "Ideas"]
    assert titles(client.get("/notes?q=plumber")) == ["Work"]
    assert titles(client.get("/notes?q=zzz")) == []
    assert len(client.get("/notes?q=").get_json()) == 3
