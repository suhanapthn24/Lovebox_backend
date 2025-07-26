from pydantic import BaseModel
from typing import Dict

class MoodEntry(BaseModel):
    date: str  
    mood: str  