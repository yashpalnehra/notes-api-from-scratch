TITLE_MAX = 100
BODY_MAX = 5000
TAG_MAX = 30
TAGS_MAX = 10
FIELDS = {"title", "body", "tags"}


def validate_note(data):
    """Problems with a posted note. An empty list means it can be stored."""
    if not isinstance(data, dict):
        return ["body must be a JSON object"]
    problems = []

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

    problems += _tag_problems(data.get("tags", []))

    unknown = set(data) - FIELDS
    if unknown:
        problems.append("unknown fields: " + ", ".join(sorted(unknown)))
    return problems


def _tag_problems(tags):
    if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
        return ["tags must be a list of strings"]
    if len(tags) > TAGS_MAX:
        return [f"at most {TAGS_MAX} tags"]
    bad = [t for t in tags if not t.strip() or len(t) > TAG_MAX or " " in t.strip()]
    if bad:
        return [f"tags must be single words of at most {TAG_MAX} characters"]
    return []


def clean_note(data):
    """The fields to store, once validate_note has passed."""
    return {
        "title": data["title"].strip(),
        "body": data.get("body", ""),
        "tags": [t.strip().lower() for t in data.get("tags", [])],
    }
