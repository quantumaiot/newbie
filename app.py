from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class NoteCreate(BaseModel):
    title: str
    content: str

class Note(NoteCreate):
    id: int

notes: list[Note] = []
next_id = 1

@app.get("/")
def home():
    return {"message": "hello coco"}

@app.get("/about")
def about():
    return {"name": "Dung", "learning": "FastAPI"}

@app.get("/notes")
def get_notes():
    return notes

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    for note in notes:
        if note.id == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")

@app.post("/notes", status_code=201)
def create_note(payload: NoteCreate) -> Note:
    global next_id
    note = Note(id=next_id, **payload.model_dump())
    notes.append(note)
    next_id += 1
    return note

@app.delete("/notes/{note_id}")
def delete_note(note_id: int) -> dict:
    for note in notes:
        if note.id == note_id:
            notes.remove(note)
            return {"deleted": note_id}
    raise HTTPException(status_code=404, detail="Note not found")