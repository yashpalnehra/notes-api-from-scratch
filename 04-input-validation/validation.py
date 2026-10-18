TITLE_MAX = 100
BODY_MAX = 5000


def validate_note(data):
    """Return a list of problems with the posted note. Empty means it is fine."""
    problems = []
    if not isinstance(data, dict):
        return ["body must be a JSON object"]

    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        problems.append("title is required")
    elif len(title) > TITLE_MAX:
        problems.append(f"title is longer than {TITLE_MAX} characters")

    body = data.get("body", "")
    if not isinstance(body, str):
        problems.append("body must be a string")
    elif len(body) > BODY_MAX:
        problems.append(f"body is longer than {BODY_MAX} characters")

    unknown = set(data) - {"title", "body"}
    if unknown:
        problems.append("unknown fields: " + ", ".join(sorted(unknown)))
    return problems
