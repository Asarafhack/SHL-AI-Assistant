from fastapi import APIRouter
from app.schemas import ChatRequest
from app.services.chat_service import process_chat

router=APIRouter()

@router.get("/health")
def health():
    return {
        "status":"ok"
    }

@router.post("/chat")
def chat(request:ChatRequest):
    return process_chat(request)