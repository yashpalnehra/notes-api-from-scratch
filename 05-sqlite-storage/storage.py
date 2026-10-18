import sqlite3

SCHEMA = """
create table if not exists notes (
    id    integer primary key autoincrement,
    title text not null,
    body  text not null default ''
)
"""


class NoteStore:
    def __init__(self, path):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute(SCHEMA)

    def add(self, title, body=""):
        cur = self.conn.execute(
            "insert into notes (title, body) values (?, ?)", (title, body)
        )
        self.conn.commit()
        return self.get(cur.lastrowid)

    def get(self, note_id):
        row = self.conn.execute(
            "select * from notes where id = ?", (note_id,)
        ).fetchone()
        return dict(row) if row else None

    def all(self):
        rows = self.conn.execute("select * from notes order by id").fetchall()
        return [dict(r) for r in rows]

    def close(self):
        self.conn.close()
