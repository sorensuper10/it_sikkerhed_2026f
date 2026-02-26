from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import requests
import json
from pathlib import Path

# uvicorn Softwaresikkerhed26022026.notes_service:app --port 8001 --reload

app = FastAPI(
    title="Notes Microservice",
    description="Microservice that only allows access if Auth-server approves the token",
    version="1.0"
)

# JSON-fil som “database”
DB_FILE = Path("notes_db.json")

# Hvis filen ikke findes, opret tom liste
if not DB_FILE.exists():
    DB_FILE.write_text(json.dumps([]))


# Pydantic model til input
class NoteIn(BaseModel):
    text: str


# Funktion der verificerer token via auth-server
def verify_token(token: str):
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    if not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    try:
        response = requests.get(
            "http://127.0.0.1:8000/users",
            headers={"token": token}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Token not authorized")

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=500,
            detail="Auth server not reachable"
        )


# Hjælpefunktioner til JSON-database
def load_notes():
    with DB_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_notes(notes):
    with DB_FILE.open("w", encoding="utf-8") as f:
        json.dump(notes, f, indent=4)


# Create note endpoint
@app.post("/notes")
def create_note(note: NoteIn, token: str = Header(...)):
    verify_token(token)

    notes = load_notes()
    new_note = {
        "id": len(notes) + 1,
        "text": note.text
    }
    notes.append(new_note)
    save_notes(notes)

    return {"status": "note created", "note": new_note}


# Get all notes endpoint
@app.get("/notes")
def get_notes(token: str = Header(...)):
    verify_token(token)
    notes = load_notes()
    return {"status": "success", "notes": notes}


# Get single note endpoint
@app.get("/notes/{note_id}")
def get_note(note_id: int, token: str = Header(...)):
    verify_token(token)
    notes = load_notes()
    for note in notes:
        if note["id"] == note_id:
            return {"status": "success", "note": note}

    raise HTTPException(status_code=404, detail="Note not found")