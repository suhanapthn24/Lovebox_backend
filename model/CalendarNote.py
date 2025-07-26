from pydantic import BaseModel
from typing import Optional

class CalendarNote(BaseModel):
    date: str  # Format: YYYY-MM-DD
    note: str
    recurring: Optional[bool] = False  # If the note repeats yearly

class UpdateNote(BaseModel):
    note: Optional[str] = None
    recurring: Optional[bool] = None