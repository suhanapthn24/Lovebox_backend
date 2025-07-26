# models/PhotoNote.py
from pydantic import BaseModel
from typing import Optional

class Note(BaseModel):
    text: str
    color: str
    sticker: Optional[str] = ""

class Photo(BaseModel):
    id: str
    # filename: str
    # caption: Optional[str] = "Untitled"
    note: Note
