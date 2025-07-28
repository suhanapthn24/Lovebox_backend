from fastapi import FastAPI
from memory_model import Memory
from typing import List
import json
import os

router = FastAPI()
MEMORY_FILE = "memories.json"

def load_memories():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memories(memories):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memories, f, indent=2)

@router.post("/memory/add")
def add_memory(memory: Memory):
    memories = load_memories()
    memories.append(memory.dict())
    save_memories(memories)
    return {"message": "Memory added"}

@router.get("/memory/{username}", response_model=List[Memory])
def get_user_memories(username: str):
    memories = load_memories()
    return [m for m in memories if m["author"] == username]