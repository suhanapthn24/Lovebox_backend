# memory_model.py
from pydantic import BaseModel

class Memory(BaseModel):
    title: str
    message: str
    mood: str
    date: str
    author: str
