from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class NoteCreate(BaseModel):
    title: str
    content: str

notes = []

@app.get("/")
def home():
    return {"message": "hello"}

@app.get("/about")
def about():
    return {"name": "Dung", "learning": "FastAPI"}

@app.get("/notes")
def get_notes():
    return notes

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    return {"note_id": note_id, "type": str(type(note_id))}

@app.post("/notes")
def create_note(note: NoteCreate):
    notes.append(note)
    return note