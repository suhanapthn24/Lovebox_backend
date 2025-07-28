from fastapi import APIRouter, HTTPException
from datetime import date
import json
import os

router = APIRouter()

NOTES_FILE = "daily_notes.json"

# Load from file or fallback to default
default_love_notes = [
    "You are someone's favorite notification. 💬💕",
    "Your smile can light up galaxies. 🌌✨",
    "You are made of magic, stardust, and love. 🌟💗",
    "You matter. Your memories matter. 💖📸",
    "Someone out there is grateful you exist. 💌",
    "You’re doing better than you think. 💞",
    "The world is better with your love in it. 🌷",
    "You make my day better 💕"
]

def load_notes():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as f:
            json.dump(default_love_notes, f)
    with open(NOTES_FILE, "r") as f:
        return json.load(f)

def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)

# GET: Daily rotating love note
@router.get("/")
def get_daily_note():
    notes = load_notes()
    today = date.today().toordinal()
    index = today % len(notes)
    return {"note": notes[index]}

# GET: All notes
@router.get("/all")
def get_all_notes():
    return {"notes": load_notes()}

# POST: Add a new love note
@router.post("/add")
def add_note(note: str):
    notes = load_notes()
    notes.append(note)
    save_notes(notes)
    return {"message": "Note added", "notes": notes}

# PUT: Edit an existing note by index
@router.put("/edit/{index}")
def edit_note(index: int, new_note: str):
    notes = load_notes()
    if index < 0 or index >= len(notes):
        raise HTTPException(status_code=404, detail="Note index out of range")
    notes[index] = new_note
    save_notes(notes)
    return {"message": "Note updated", "notes": notes}

# DELETE: Delete a note by index
@router.delete("/delete/{index}")
def delete_note(index: int):
    notes = load_notes()
    if index < 0 or index >= len(notes):
        raise HTTPException(status_code=404, detail="Note index out of range")
    removed = notes.pop(index)
    save_notes(notes)
    return {"message": "Note deleted", "removed_note": removed, "notes": notes}
