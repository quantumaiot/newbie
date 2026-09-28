from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row
from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    db_url: str
    model_config = SettingsConfigDict(env_file=".env")


settings = Setting()

app = FastAPI()

class NoteCreate(BaseModel):
    title: str
    content: str

class Note(NoteCreate):
    id: int

@app.get("/")
def home():
    return {"message": "hello"}

@app.get("/notes")
def get_notes() -> list[Note]:
    with psycopg.connect(settings.db_url, row_factory=dict_row) as conn:
        list_note = conn.execute("SELECT * FROM notes").fetchall()
    return list_note 

@app.get("/notes/{note_id}")
def get_note(note_id: int) -> Note:
    with psycopg.connect(settings.db_url, row_factory=dict_row) as conn:
        note = conn.execute("SELECT * FROM notes WHERE id = %s", (note_id,)).fetchone()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
    
@app.post("/notes", status_code=201)
def create_note(payload: NoteCreate) -> Note:
    with psycopg.connect(settings.db_url, row_factory=dict_row) as conn:
        note = conn.execute(
            "INSERT INTO notes (title, content) VALUES (%s, %s) RETURNING *", 
            (payload.title, payload.content),
            ).fetchone()
    return note

@app.put("/notes/{note_id}")
def update_note(note_id: int, payload: NoteCreate) -> Note:
    with psycopg.connect(settings.db_url, row_factory=dict_row) as conn:
        note = conn.execute(
            "UPDATE notes SET (title, content) = (%s, %s) WHERE id = %s RETURNING *",
            (payload.title, payload.content, note_id),
            ).fetchone()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.delete("/notes/{note_id}")
def delete_note(note_id: int) -> dict:
    with psycopg.connect(settings.db_url, row_factory=dict_row) as conn:
        count = conn.execute("DELETE FROM notes WHERE id = %s", (note_id,)).rowcount
    if count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return {"deleted": note_id}