import sqlite3
from datetime import datetime, timezone

SCHEMA = """
create table if not exists notes (
    id         integer primary key autoincrement,
    title      text not null,
    body       text not null default '',
    created_at text not null,
    updated_at text not null
);
create table if not exists note_tags (
    note_id integer not null references notes(id) on delete cascade,
    tag     text not null,
    primary key (note_id, tag)
);
"""


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class NoteStore:
    def __init__(self, path):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("pragma foreign_keys = on")
        self.conn.executescript(SCHEMA)

    def add(self, title, body="", tags=()):
        stamp = now()
        cur = self.conn.execute(
            "insert into notes (title, body, created_at, updated_at) values (?, ?, ?, ?)",
            (title, body, stamp, stamp),
        )
        self._set_tags(cur.lastrowid, tags)
        self.conn.commit()
        return self.get(cur.lastrowid)

    def get(self, note_id):
        row = self.conn.execute(
            "select * from notes where id = ?", (note_id,)
        ).fetchone()
        return self._with_tags(row) if row else None

    def list(self, query="", tag="", limit=50, offset=0):
        sql = "select distinct n.* from notes n"
        where = []
        params = []
        if tag:
            sql += " join note_tags t on t.note_id = n.id"
            where.append("t.tag = ?")
            params.append(tag)
        if query:
            where.append("(n.title like ? or n.body like ?)")
            params += [f"%{query}%", f"%{query}%"]
        if where:
            sql += " where " + " and ".join(where)
        sql += " order by n.id limit ? offset ?"
        rows = self.conn.execute(sql, [*params, limit, offset]).fetchall()
        return [self._with_tags(r) for r in rows]

    def count(self):
        return self.conn.execute("select count(*) from notes").fetchone()[0]

    def update(self, note_id, title, body, tags=()):
        cur = self.conn.execute(
            "update notes set title = ?, body = ?, updated_at = ? where id = ?",
            (title, body, now(), note_id),
        )
        if cur.rowcount == 0:
            return None
        self._set_tags(note_id, tags)
        self.conn.commit()
        return self.get(note_id)

    def delete(self, note_id):
        cur = self.conn.execute("delete from notes where id = ?", (note_id,))
        self.conn.commit()
        return cur.rowcount == 1

    def _set_tags(self, note_id, tags):
        self.conn.execute("delete from note_tags where note_id = ?", (note_id,))
        self.conn.executemany(
            "insert into note_tags (note_id, tag) values (?, ?)",
            [(note_id, tag) for tag in sorted(set(tags))],
        )

    def _with_tags(self, row):
        note = dict(row)
        rows = self.conn.execute(
            "select tag from note_tags where note_id = ? order by tag", (note["id"],)
        ).fetchall()
        note["tags"] = [r["tag"] for r in rows]
        return note

    def close(self):
        self.conn.close()
