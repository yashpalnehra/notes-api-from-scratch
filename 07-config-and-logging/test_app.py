import logging

import pytest

from app import create_app
from config import Config, from_env


@pytest.fixture
def client(tmp_path):
    return create_app(Config(db_path=str(tmp_path / "test.db"))).test_client()


def test_config_defaults():
    cfg = from_env({})
    assert cfg == Config(
        db_path="notes.db", host="127.0.0.1", port=8000, log_level="INFO"
    )


def test_config_from_env():
    cfg = from_env(
        {"NOTES_DB": "/tmp/x.db", "NOTES_PORT": "9000", "NOTES_LOG_LEVEL": "debug"}
    )
    assert cfg.db_path == "/tmp/x.db"
    assert cfg.port == 9000
    assert cfg.log_level == "DEBUG"


def test_config_rejects_bad_port():
    with pytest.raises(ValueError, match="NOTES_PORT"):
        from_env({"NOTES_PORT": "eighty"})
    with pytest.raises(ValueError, match="NOTES_PORT"):
        from_env({"NOTES_PORT": "70000"})


def test_health(client):
    client.post("/notes", json={"title": "a"})
    assert client.get("/health").get_json() == {"status": "ok", "notes": 1}


def test_unknown_route_is_json(client):
    resp = client.get("/nothing-here")
    assert resp.status_code == 404
    assert "errors" in resp.get_json()


def test_wrong_method_is_json(client):
    resp = client.patch("/notes")
    assert resp.status_code == 405
    assert "errors" in resp.get_json()


def test_requests_are_logged(client, caplog):
    with caplog.at_level(logging.INFO, logger="notes"):
        client.post("/notes", json={"title": "a"})
        client.get("/notes/1")
    messages = [r.getMessage() for r in caplog.records]
    assert any(m.startswith("POST /notes 201") for m in messages)
    assert any(m.startswith("GET /notes/1 200") for m in messages)
    assert "created note 1" in messages
