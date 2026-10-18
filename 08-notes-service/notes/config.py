import os
from dataclasses import dataclass


@dataclass
class Config:
    db_path: str = "notes.db"
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "INFO"
    page_size: int = 50


def from_env(env=None):
    """Read NOTES_* variables. Anything missing keeps its default."""
    env = os.environ if env is None else env
    return Config(
        db_path=env.get("NOTES_DB", "notes.db"),
        host=env.get("NOTES_HOST", "127.0.0.1"),
        port=_int(env, "NOTES_PORT", 8000, 1, 65535),
        log_level=env.get("NOTES_LOG_LEVEL", "INFO").upper(),
        page_size=_int(env, "NOTES_PAGE_SIZE", 50, 1, 500),
    )


def _int(env, name, default, low, high):
    raw = env.get(name)
    if raw is None:
        return default
    if not raw.isdigit() or not low <= int(raw) <= high:
        raise ValueError(f"{name} must be a number from {low} to {high}, got {raw!r}")
    return int(raw)
