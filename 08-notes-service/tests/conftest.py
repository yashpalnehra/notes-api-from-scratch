import pytest

from notes import create_app
from notes.config import Config
from notes.storage import NoteStore


@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "test.db")


@pytest.fixture
def store(db_path):
    s = NoteStore(db_path)
    yield s
    s.close()


@pytest.fixture
def client(db_path):
    return create_app(Config(db_path=db_path)).test_client()
