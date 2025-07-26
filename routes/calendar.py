from fastapi import APIRouter, HTTPException, Depends
from model.CalendarNote import CalendarNote, UpdateNote
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import json
import os

router = APIRouter()

DB_FILE = "database.json"


SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_username(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# DB helpers
def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ----------- Routes ----------- #

# Get all notes for a specific month
@router.get("/calendar/{year}/{month}")
def get_events(year: int, month: int):
    db = load_db()
    month_events = {}

    for date, entry in db.items():
        y, m, d = date.split("-")
        if int(y) == year and int(m) == month:
            month_events[date] = entry
        elif entry.get("recurring") and int(m) == month:
            recurring_date = f"{year}-{m.zfill(2)}-{d.zfill(2)}"
            month_events[recurring_date] = entry

    return month_events

# Get note for a specific date
@router.get("/calendar/date/{date}")
def get_note_by_date(date: str):
    db = load_db()
    note = db.get(date)
    if note:
        return note
    else:
        raise HTTPException(status_code=404, detail="Note not found.")

# Add a new note
@router.post("/calendar/add")
def add_note(note: CalendarNote):
    db = load_db()
    if note.date in db:
        raise HTTPException(status_code=400, detail="Note already exists for that date.")
    db[note.date] = note.dict()
    save_db(db)
    return {"message": "Note added successfully."}

# Update an existing note
@router.put("/calendar/update/{date}")
def update_note(date: str, note: UpdateNote):
    db = load_db()
    if date not in db:
        raise HTTPException(status_code=404, detail="Note not found.")
    
    db[date].update({k: v for k, v in note.dict().items() if v is not None})
    save_db(db)
    return {"message": "Note updated successfully."}

# Delete a note
@router.delete("/calendar/delete/{date}")
def delete_note(date: str):
    db = load_db()
    if date not in db:
        raise HTTPException(status_code=404, detail="Note not found.")
    del db[date]
    save_db(db)
    return {"message": "Note deleted successfully."}