# mood_api.py
from fastapi import APIRouter, HTTPException
from model.mode import MoodEntry
from pathlib import Path
from typing import Dict
import json
import os

router = APIRouter()

MOOD_FILE = Path("mood_data.json")

# Load or initialize the mood file
def load_moods() -> Dict[str, str]:
    if not os.path.exists(MOOD_FILE):
        return {}
    with open(MOOD_FILE, "r") as f:
        return json.load(f)

def save_moods(moods: Dict[str, str]):
    with open(MOOD_FILE, "w") as f:
        json.dump(moods, f, indent=2)

# POST /moods/add
@router.post("/mood/add")
def add_mood(entry: MoodEntry):
    moods = load_moods()
    if entry.date in moods:
        raise HTTPException(status_code=400, detail="Mood for this date already exists.")
    moods[entry.date] = entry.mood
    save_moods(moods)
    return {"message": "Mood added successfully."}

# GET /moods/date/{date}
@router.get("/mood/date/{date}")
def get_mood(date: str):
    moods = load_moods()
    mood = moods.get(date)
    if not mood:
        raise HTTPException(status_code=404, detail="No mood found for this date.")
    return {"date": date, "mood": mood}

# PUT /moods/update/{date}
@router.put("/mood/update/{date}")
def update_mood(date: str, entry: MoodEntry):
    moods = load_moods()
    if date not in moods:
        raise HTTPException(status_code=404, detail="Mood not found.")
    moods[date] = entry.mood
    save_moods(moods)
    return {"message": "Mood updated successfully."}

@router.delete("/mood/delete/{date_str}")
def delete_mood(date_str: str):
    if MOOD_FILE.exists():
        with open(MOOD_FILE, "r") as f:
            mood_data = json.load(f)
    else:
        mood_data = {}

    if date_str in mood_data:
        del mood_data[date_str]
        with open(MOOD_FILE, "w") as f:
            json.dump(mood_data, f, indent=2)
        return {"message": "Mood deleted"}
    else:
        return {"message": "No mood found for this date"}

# GET /moods/{year}/{month}
@router.get("/mood/{year}/{month}")
def get_monthly_moods(year: int, month: int):
    moods = load_moods()
    prefix = f"{year}-{month:02d}"
    monthly_moods = {date: mood for date, mood in moods.items() if date.startswith(prefix)}
    return monthly_moods
