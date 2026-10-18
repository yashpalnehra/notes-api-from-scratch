from notes.validation import clean_note, validate_note


def test_minimal_note_is_fine():
    assert validate_note({"title": "x"}) == []


def test_full_note_is_fine():
    assert validate_note({"title": "x", "body": "y", "tags": ["work", "Urgent"]}) == []


def test_title_rules():
    assert validate_note({}) == ["title is required"]
    assert validate_note({"title": " "}) == ["title is required"]
    assert validate_note({"title": "a" * 101}) == [
        "title is longer than 100 characters"
    ]


def test_tag_rules():
    assert validate_note({"title": "x", "tags": "work"}) == [
        "tags must be a list of strings"
    ]
    assert validate_note({"title": "x", "tags": [1]}) == [
        "tags must be a list of strings"
    ]
    assert validate_note({"title": "x", "tags": ["two words"]}) == [
        "tags must be single words of at most 30 characters"
    ]
    assert validate_note({"title": "x", "tags": [""]}) == [
        "tags must be single words of at most 30 characters"
    ]
    assert validate_note({"title": "x", "tags": ["t"] * 11}) == ["at most 10 tags"]


def test_unknown_fields_reported_after_other_problems():
    assert validate_note({"body": 1, "x": 1}) == [
        "title is required",
        "body must be a string",
        "unknown fields: x",
    ]


def test_clean_note():
    assert clean_note({"title": " Hi ", "tags": [" Work", "HOME"]}) == {
        "title": "Hi",
        "body": "",
        "tags": ["work", "home"],
    }
