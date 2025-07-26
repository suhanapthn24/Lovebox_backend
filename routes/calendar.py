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

# ---------------------- Helpers ---------------------- #

def get_current_username(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ---------------------- Routes ---------------------- #

@router.get("/calendar/{year}/{month}")
def get_events(year: int, month: int, username: str = Depends(get_current_username)):
    db = load_db()
    month_events = {}

    for date, entry in db.items():
        y, m, d = date.split("-")
        if entry.get("user") != username and username not in entry.get("shared_with", []):
            continue  # skip others' notes

        if int(y) == year and int(m) == month:
            month_events[date] = entry
        elif entry.get("recurring") and int(m) == month:
            recurring_date = f"{year}-{m.zfill(2)}-{d.zfill(2)}"
            month_events[recurring_date] = entry

    return month_events


@router.get("/calendar/date/{date}")
def get_note_by_date(date: str, username: str = Depends(get_current_username)):
    db = load_db()
    note = db.get(date)

    if note and (note.get("user") == username or username in note.get("shared_with", [])):
        return note
    raise HTTPException(status_code=404, detail="Note not found.")


@router.post("/calendar/add")
def add_note(note: CalendarNote, username: str = Depends(get_current_username)):
    db = load_db()
    if note.date in db:
        raise HTTPException(status_code=400, detail="Note already exists for that date.")
    
    db[note.date] = note.dict()
    db[note.date]["user"] = username
    save_db(db)
    return {"message": "Note added successfully."}


@router.put("/calendar/update/{date}")
def update_note(date: str, note: UpdateNote, username: str = Depends(get_current_username)):
    db = load_db()
    if date not in db:
        raise HTTPException(status_code=404, detail="Note not found.")

    # Allow update if user is owner or in shared_with list
    if db[date].get("user") != username and username not in db[date].get("shared_with", []):
        raise HTTPException(status_code=403, detail="Unauthorized to update this note.")
    
    for k, v in note.dict().items():
        if v is not None:
            db[date][k] = v

    save_db(db)
    return {"message": "Note updated successfully."}


@router.delete("/calendar/delete/{date}")
def delete_note(date: str, username: str = Depends(get_current_username)):
    db = load_db()
    if date not in db:
        raise HTTPException(status_code=404, detail="Note not found.")
    if db[date].get("user") != username:
        raise HTTPException(status_code=403, detail="Only the owner can delete this note.")
    
    del db[date]
    save_db(db)
    return {"message": "Note deleted successfully."}
