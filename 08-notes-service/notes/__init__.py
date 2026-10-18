import logging
import time

from flask import Flask, g, jsonify, request
from werkzeug.exceptions import HTTPException

from notes.config import Config
from notes.routes import api
from notes.storage import NoteStore

log = logging.getLogger("notes")


def create_app(config=None):
    config = config or Config()
    app = Flask(__name__)
    app.config["STORE"] = NoteStore(config.db_path)
    app.config["PAGE_SIZE"] = config.page_size
    app.register_blueprint(api)
    log.info("using database %s", config.db_path)

    @app.before_request
    def start_timer():
        g.started = time.perf_counter()

    @app.after_request
    def log_request(response):
        ms = (time.perf_counter() - g.started) * 1000
        log.info(
            "%s %s %s %.1fms", request.method, request.path, response.status_code, ms
        )
        return response

    @app.errorhandler(HTTPException)
    def http_error(e):
        return jsonify({"errors": [e.description]}), e.code

    @app.errorhandler(Exception)
    def unexpected_error(e):
        log.exception("unhandled error on %s %s", request.method, request.path)
        return jsonify({"errors": ["internal error"]}), 500

    return app
