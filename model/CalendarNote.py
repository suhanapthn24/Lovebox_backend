from pydantic import BaseModel
from typing import Optional, List

class CalendarNote(BaseModel):
    date: str
    title: str
    text: str
    recurring: Optional[bool] = False
    shared_with: Optional[List[str]] = []  # 👈 NEW field


class UpdateNote(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    recurring: Optional[bool] = None
    shared_with: Optional[List[str]] = None  # 👈 NEW field
