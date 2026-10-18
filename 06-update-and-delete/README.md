# Update and delete

The full set of routes.

    GET    /notes            all notes
    GET    /notes?q=milk     notes with milk in the title or body
    POST   /notes            create
    GET    /notes/<id>       read
    PUT    /notes/<id>       replace title and body, same validation as POST
    DELETE /notes/<id>       remove, returns 204

POST and PUT share `read_note_json`, so the validation only lives in one place. Run with `python3 app.py`, test with `python3 -m pytest`.
