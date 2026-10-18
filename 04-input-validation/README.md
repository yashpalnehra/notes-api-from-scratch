# Input validation

Same API as folder 03, but a bad POST now gets a 400 with a list of what's wrong instead of being stored as-is. The rules live in `validation.py` so they can be tested on their own. A title is required and at most 100 characters, the body is optional and at most 5000, and unknown fields are rejected.

Errors always come back in the same shape, `{"errors": [...]}`, including the 404.

Run with `python3 app.py`. Tests: `python3 -m pytest`.
