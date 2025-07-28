from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router
from routes.photonote import router as note_router
from routes.upload import router as upload_router
from routes.lovenote import router as daily_router
from routes.calendar import router as calendar_router
from routes.mood_api import router as mood_router
from routes.doodle_api import router as doodle_router
from routes.memory_model import router as memory_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# CORS for frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving for uploaded images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Routers with clean prefixes
# app.include_router(photo_router, prefix="/photo")
app.include_router(auth_router, tags=['Authentication'])
app.include_router(calendar_router, tags=['Calendar'])
app.include_router(daily_router, prefix="/daily-note", tags=['Daily Notes'])
app.include_router(doodle_router, tags=['Doodle'])
app.include_router(memory_router, tags=['Memory Jar'])
app.include_router(mood_router, tags=['Mood'])
app.include_router(note_router, tags=['Note'])
app.include_router(upload_router, tags=['Uploads'])