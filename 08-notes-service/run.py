import logging
import sys

from notes import create_app
from notes.config import from_env


def main():
    try:
        config = from_env()
    except ValueError as e:
        print(f"bad configuration: {e}", file=sys.stderr)
        sys.exit(2)
    logging.basicConfig(
        level=config.log_level, format="%(asctime)s %(levelname)s %(message)s"
    )
    create_app(config).run(host=config.host, port=config.port)


if __name__ == "__main__":
    main()
