import psycopg
from psycopg.rows import dict_row

with psycopg.connect("postgresql://noteuser@localhost:5432/notesdb", row_factory=dict_row) as conn:
    rows = conn.execute("SELECT * FROM notes").fetchall()
    note = conn.execute("SELECT * FROM notes WHERE id = %s", (3,)).fetchone()
    print(note)