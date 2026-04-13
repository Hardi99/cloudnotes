from fastapi import APIRouter, HTTPException
from azure.cosmos.exceptions import CosmosHttpResponseError
from .cosmos import get_container
from .models import NoteCreateRequest, AttachmentRequest, note_to_entity
from .blob_service import generate_upload_sas

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("", status_code=201)
def create_note(req: NoteCreateRequest):
    container = get_container()
    entity = note_to_entity(req)
    try:
        container.create_item(body=entity)
    except CosmosHttpResponseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return entity

@router.get("")
def list_notes():
    container = get_container()
    items = list(container.query_items(
        query="SELECT * FROM c WHERE c.pk = 'NOTE' ORDER BY c.createdAt DESC",
        enable_cross_partition_query=True
    ))
    return items

@router.get("/{note_id}")
def get_note(note_id: str):
    container = get_container()
    try:
        return container.read_item(item=note_id, partition_key="NOTE")
    except CosmosHttpResponseError as e:
        if getattr(e, "status_code", None) == 404:
            raise HTTPException(status_code=404, detail="Note not found")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: str):
    container = get_container()
    try:
        container.delete_item(item=note_id, partition_key="NOTE")
    except CosmosHttpResponseError as e:
        if getattr(e, "status_code", None) == 404:
            raise HTTPException(status_code=404, detail="Note not found")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{note_id}/attachments")
def get_attachment_url(note_id: str, req: AttachmentRequest):
    blob_path = f"{note_id}/{req.fileName}"
    upload_url = generate_upload_sas(blob_path)
    return {"uploadUrl": upload_url, "blobPath": blob_path}
