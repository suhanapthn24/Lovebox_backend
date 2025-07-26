# routes/doodle_api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import json

router = APIRouter()

DOODLE_FILE = Path("doodles.json")

class DoodleEntry(BaseModel):
    date: str
    image_data: str  # base64 encoded PNG

@router.post("/doodle/save")
def save_doodle(entry: DoodleEntry):
    data = {}
    if DOODLE_FILE.exists():
        with open(DOODLE_FILE, "r") as f:
            data = json.load(f)
    data[entry.date] = entry.image_data
    with open(DOODLE_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return {"message": "Doodle saved"}

@router.get("/doodle/{date}")
def get_doodle(date: str):
    if not DOODLE_FILE.exists():
        return {"image_data": None}
    with open(DOODLE_FILE, "r") as f:
        data = json.load(f)
    return {"image_data": data.get(date)}
