from fastapi import APIRouter, UploadFile, File, Form
from pathlib import Path
import os
import json
from fastapi.responses import JSONResponse

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

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


@router.get("/upload")
async def get_uploaded_photos(user: str = None, album: str = None):
    """Return images uploaded by or shared with the user, optionally filtered by album."""
    photo_list = []
    metadata = load_metadata()

    for filename in os.listdir(UPLOAD_DIR):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            note = metadata.get(filename, {})
            owner = note.get("user")
            shared_with = note.get("shared_with", [])
            photo_album = note.get("album")

            # Filter by user
            if user and user != owner and user not in shared_with:
                continue
            # Filter by album
            if album and album != photo_album:
                continue

            photo_list.append({
                "filename": filename,
                "url": f"/uploads/{filename}",
                "note": note
            })

    return photo_list


@router.post("/upload/")
async def upload_image(
    file: UploadFile = File(...),
    note: str = Form(""),
    color: str = Form("black"),
    sticker: str = Form(""),
    username: str = Form(...),
    shared_with: str = Form(""),  # comma-separated list of usernames
    album: str = Form("")         # optional album name
):
    file_path = UPLOAD_DIR / file.filename

    # Save image
    with file_path.open("wb") as f:
        f.write(await file.read())

    metadata = load_metadata()
    shared_users = [u.strip() for u in shared_with.split(",") if u.strip()]
    metadata[file.filename] = {
        "user": username,
        "shared_with": shared_users,
        "album": album,
        "text": note,
        "color": color,
        "sticker": sticker,
    }
    save_metadata(metadata)

    return JSONResponse({
        "filename": file.filename,
        "url": f"/uploads/{file.filename}",
        "note": metadata[file.filename]
    })
