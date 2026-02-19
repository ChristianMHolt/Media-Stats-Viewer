from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os

from .scanner import scan_library
from .models import MediaItem

app = FastAPI(title="Media Library Tracker")

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/scan", response_model=List[MediaItem])
async def scan_endpoint(path: str):
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Path not found")

    try:
        items = scan_library(path)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
