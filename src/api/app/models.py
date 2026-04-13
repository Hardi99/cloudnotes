from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional
import uuid

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

class NoteCreateRequest(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(default="")

class AttachmentRequest(BaseModel):
    fileName: str
    contentType: str = "application/octet-stream"

def note_to_entity(req: NoteCreateRequest) -> dict:
    note_id = str(uuid.uuid4())
    ts = now_iso()
    return {
        "id": note_id,
        "pk": "NOTE",
        "title": req.title,
        "content": req.content,
        "createdAt": ts,
        "updatedAt": ts,
        "attachments": []
    }
