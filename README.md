# Notes API from scratch

A small HTTP service for keeping notes, built up one step at a time. The first two folders use only the standard library. From folder 03 on it's Flask with SQLite, and the last folder is the complete service with config, logging and a test suite. Everything listens on 127.0.0.1 and is meant to run on your own machine.

1. `01-hello-server`, a server that says hello, standard library only.
2. `02-json-routes`, a route table and JSON responses, first tests.
3. `03-notes-in-memory`, first Flask app, notes kept in a dict.
4. `04-input-validation`, bad input gets a 400 with a list of problems.
5. `05-sqlite-storage`, notes survive a restart.
6. `06-update-and-delete`, the full set of routes plus search.
7. `07-config-and-logging`, settings from the environment, request logs, JSON errors everywhere.
8. `08-notes-service`, the finished service as a package, with tags and paging.

## Setup

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Then cd into a folder and follow its README. Each folder's tests run with `python3 -m pytest` from inside that folder. Folders 05 to 08 create a `notes.db` file when you run the server, which git ignores.
