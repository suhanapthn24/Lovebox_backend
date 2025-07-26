from fastapi import APIRouter
from model.PhotoNote import Photo
from pathlib import Path
import json

router = APIRouter()

UPLOAD_DIR = Path("uploads")
META_FILE = UPLOAD_DIR / "metadata.json"

if not META_FILE.exists():
    META_FILE.write_text("{}")


def load_metadata():
    try:
        with open(META_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_metadata(data):
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


@router.post("/note/")
def save_note(note: Photo):
    metadata = load_metadata()
    metadata[note.id] = note.note.dict()
    save_metadata(metadata)
    return {"message": "Note saved!", "note": metadata[note.id]}


@router.get("/note/{photo_id}")
def get_note(photo_id: str):
    metadata = load_metadata()
    return {"note": metadata.get(photo_id, {
        "text": "",
        "color": "black",
        "sticker": ""
    })}


@router.get("/notes/")
def get_all_notes():
    return load_metadata()
