def test_add_and_get(store):
    note = store.add("first", "hello", ["b", "a", "a"])
    assert note["id"] == 1
    assert note["tags"] == ["a", "b"]
    assert note["created_at"] == note["updated_at"]
    assert store.get(1) == note
    assert store.get(2) is None


def test_update_changes_tags_and_timestamp(store):
    note = store.add("t", "b", ["old"])
    updated = store.update(note["id"], "t2", "b2", ["new"])
    assert (updated["title"], updated["body"], updated["tags"]) == ("t2", "b2", ["new"])
    assert updated["created_at"] == note["created_at"]
    assert store.update(99, "x", "y") is None


def test_delete_removes_tags_too(store):
    note = store.add("t", tags=["x"])
    assert store.delete(note["id"])
    assert not store.delete(note["id"])
    assert store.conn.execute("select count(*) from note_tags").fetchone()[0] == 0


def test_list_filters(store):
    store.add("Shopping", "eggs and milk", ["home"])
    store.add("Standup", "talk about eggs", ["work"])
    store.add("Gym", "", ["home", "health"])
    titles = lambda notes: [n["title"] for n in notes]
    assert titles(store.list()) == ["Shopping", "Standup", "Gym"]
    assert titles(store.list(query="eggs")) == ["Shopping", "Standup"]
    assert titles(store.list(tag="home")) == ["Shopping", "Gym"]
    assert titles(store.list(query="eggs", tag="home")) == ["Shopping"]
    assert titles(store.list(limit=1, offset=1)) == ["Standup"]
    assert store.count() == 3
