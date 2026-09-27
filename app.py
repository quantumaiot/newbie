from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "hello"}

@app.get("/about")
def about():
    return {"name": "Dung", "learning": "FastAPI"}

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    return {"note_id": note_id, "type": str(type(note_id))}