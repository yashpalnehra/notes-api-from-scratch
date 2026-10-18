import pytest

from notes.config import Config, from_env


def make(client, title, **extra):
    resp = client.post("/notes", json={"title": title, **extra})
    assert resp.status_code == 201, resp.get_json()
    return resp.get_json()


def test_create_read_update_delete(client):
    note = make(client, "Plan", body="write tests", tags=["Work"])
    assert note["tags"] == ["work"]

    got = client.get(f"/notes/{note['id']}")
    assert got.status_code == 200
    assert got.get_json()["title"] == "Plan"

    put = client.put(f"/notes/{note['id']}", json={"title": "Plan v2", "tags": []})
    assert put.status_code == 200
    assert put.get_json()["tags"] == []

    assert client.delete(f"/notes/{note['id']}").status_code == 204
    assert client.get(f"/notes/{note['id']}").status_code == 404


def test_list_with_filters_and_paging(client):
    make(client, "a", tags=["x"])
    make(client, "b", tags=["y"])
    make(client, "c", tags=["x"])

    body = client.get("/notes?tag=x").get_json()
    assert [n["title"] for n in body["notes"]] == ["a", "c"]

    body = client.get("/notes?limit=1&offset=1").get_json()
    assert [n["title"] for n in body["notes"]] == ["b"]
    assert (body["limit"], body["offset"]) == (1, 1)


def test_bad_paging_is_400(client):
    assert client.get("/notes?limit=abc").status_code == 400
    assert client.get("/notes?limit=0").status_code == 400
    assert client.get("/notes?offset=-1").status_code == 400


def test_validation_errors(client):
    resp = client.post("/notes", json={"title": "", "tags": ["a b"]})
    assert resp.status_code == 400
    assert resp.get_json()["errors"] == [
        "title is required",
        "tags must be single words of at most 30 characters",
    ]
    assert client.post("/notes", data="plain text").status_code == 400


def test_errors_are_json_everywhere(client):
    missing = client.get("/missing")
    assert missing.status_code == 404
    assert list(missing.get_json()) == ["errors"]
    assert client.patch("/notes").status_code == 405
    assert "errors" in client.patch("/notes").get_json()


def test_default_page_size_comes_from_config(db_path):
    from notes import create_app

    client = create_app(Config(db_path=db_path, page_size=2)).test_client()
    for title in "abc":
        make(client, title)
    body = client.get("/notes").get_json()
    assert [n["title"] for n in body["notes"]] == ["a", "b"]
    assert body["limit"] == 2


def test_health(client):
    make(client, "a")
    assert client.get("/health").get_json() == {"status": "ok", "notes": 1}


def test_config_from_env():
    cfg = from_env({"NOTES_PORT": "9001", "NOTES_PAGE_SIZE": "20", "NOTES_DB": "x.db"})
    assert cfg == Config(db_path="x.db", port=9001, page_size=20)
    with pytest.raises(ValueError, match="NOTES_PAGE_SIZE"):
        from_env({"NOTES_PAGE_SIZE": "0"})
