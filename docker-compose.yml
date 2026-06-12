from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import get_current_user
from app.models import User
from app.schemas import ChatRequest, ChatResponse, ErrorResponse
from app.config import settings
import anthropic

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("", response_model=ChatResponse, responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def chat(request: ChatRequest, current_user: User = Depends(get_current_user)):
    if not request.message.strip():
        raise HTTPException(400, detail="Message cannot be empty")
    if not settings.ANTHROPIC_API_KEY:
        raise HTTPException(503, detail="AI service not configured")
    try:
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            system="You are AsifEdA, a helpful AI assistant for competitive exam preparation.",
            messages=[{"role": "user", "content": request.message}]
        )
        reply = response.content[0].text
    except Exception as e:
        raise HTTPException(500, detail=f"AI error: {str(e)}")
    return ChatResponse(reply=reply)
