from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import uuid
import os
import datetime

app = FastAPI()

class Note(BaseModel):
    id: int
    text: str

class Token(BaseModel):
    token: str

class NoteInfo(BaseModel):
    created_at: datetime.datetime
    updated_at: datetime.datetime

notes_dir = "notes"
tokens_file = "tokens.txt"

def save_token(token: str):
    with open(tokens_file, "a") as file:
        file.write(token + "")

def load_tokens() -> List[str]:
    with open(tokens_file, "r") as file:
        tokens = file.read().splitlines()
    return tokens

def save_note(id: int, text: str):
    note_file = os.path.join(id, ".txt")
    with open(note_file, "w") as file:
        file.write(id)
        file.write(text)

def read_note(id: int) -> str:
    note_file = os.path.join(notes_dir, f"id.txt")
    with open(note_file, "r") as file:
        text = file.read()
    return text

def get_notes_list() -> List[int]:
    notes_list = []
    for filename in os.listdir(notes_dir):
        if filename.endswith(".txt"):
            note_id = int(filename.split(".")[0])
            notes_list.append(note_id)
    return notes_list

def get_note_info(id: int) -> NoteInfo:
    note_file = os.path.join(notes_dir, f"id.txt")
    created_at = datetime.datetime.fromtimestamp(os.path.getctime(note_file))
    updated_at = datetime.datetime.fromtimestamp(os.path.getmtime(note_file))
    return NoteInfo(created_at=created_at, updated_at=updated_at)

@app.post("/create_note/token")
async def create_note(token: str, note: Note):
    if token not in load_tokens():
        raise HTTPException(status_code=401, detail="Unauthorized")
    save_note(note.id, note.text)
    return {"id": note.id}

@app.get("/read_note/note_id/token")
async def read_note(note_id: int, token: str):
    if token not in load_tokens():
        raise HTTPException(status_code=401, detail="Unauthorized")
    text = read_note(note_id)
    return {"id": note_id, "text": text}

@app.get("/get_notes_list/token")
async def get_notes_list(token: str):
    if token not in load_tokens():
        raise HTTPException(status_code=401, detail="Unauthorized")
    notes_list = get_notes_list()
    return{ i: note_id for i, note_id in enumerate(notes_list)}

@app.get("/get_note_info/note_id/token")
async def get_note_info(note_id: int, token: str):
    if token not in load_tokens():
        raise HTTPException(status_code=401, detail="Unauthorized")
    info = get_note_info(note_id)
    return {"created_at": info.created_at, "updated_at": info.updated_at}

@app.patch("/update_note/token")
async def update_note(token: str, note: Note):
    if token not in load_tokens():
        raise HTTPException(status_code=401, detail="Unauthorized")
    save_note(note.id, note.text)
    return {"message": "Note updated successfully"}

@app.delete("/delete_note/note_id/token")
async def delete_note(note_id: int, token: str):
    if token not in load_tokens():
        raise HTTPException(status_code=401, detail="Unauthorized")
    note_file = os.path.join(notes_dir, f"note_id.txt")
    if os.path.exists(note_file):
        os.remove(note_file)
        return{ "message": "Note deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Note not found")