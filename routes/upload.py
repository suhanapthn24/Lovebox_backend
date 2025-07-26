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
async def get_uploaded_photos():
    """Return a list of uploaded images with notes."""
    photo_list = []
    metadata = load_metadata()
    for filename in os.listdir(UPLOAD_DIR):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            photo_list.append({
                "filename": filename,
                "url": f"/uploads/{filename}",
                "note": metadata.get(filename, {
                    "text": "",
                    "color": "black",
                    "sticker": ""
                })
            })
    return photo_list


@router.post("/upload/")
async def upload_image(
    file: UploadFile = File(...),
    note: str = Form(""),
    color: str = Form("black"),
    sticker: str = Form("")
):
    file_path = UPLOAD_DIR / file.filename

    # Save image file
    with file_path.open("wb") as f:
        f.write(await file.read())

    # Save metadata
    metadata = load_metadata()
    metadata[file.filename] = {
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
