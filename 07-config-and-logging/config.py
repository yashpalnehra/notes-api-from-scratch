import os
from dataclasses import dataclass


@dataclass
class Config:
    db_path: str = "notes.db"
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "INFO"


def from_env(env=None):
    """Build a Config from NOTES_* variables, falling back to the defaults."""
    env = os.environ if env is None else env
    port = env.get("NOTES_PORT", "8000")
    if not port.isdigit() or not 0 < int(port) < 65536:
        raise ValueError(f"NOTES_PORT must be a port number, got {port!r}")
    return Config(
        db_path=env.get("NOTES_DB", "notes.db"),
        host=env.get("NOTES_HOST", "127.0.0.1"),
        port=int(port),
        log_level=env.get("NOTES_LOG_LEVEL", "INFO").upper(),
    )
