from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router as notes_router

app = FastAPI(title="CloudNotes API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes_router)

@app.get("/health")
def health():
    return {"status": "ok"}
