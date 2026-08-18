from fastapi import APIRouter, UploadFile, File
from app.services.upload_services import save_pdf

router = APIRouter(tags=["Upload"])

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return await save_pdf(file)
    