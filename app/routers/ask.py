from fastapi import APIRouter
from app.schemas.ask import AskRequest
from app.services.rag_service import ask_rag

router = APIRouter()

@router.post("/ask")
async def ask_question(request: AskRequest):
    return ask_rag(request)