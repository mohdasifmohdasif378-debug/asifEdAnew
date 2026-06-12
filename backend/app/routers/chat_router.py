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
        # Local 'study' assistant fallback: analyze project source under the
        # backend `app/` directory and return helpful, contextual replies.
        from pathlib import Path
        import re

        msg_lower = request.message.strip().lower()
        # handle simple greetings without echoing
        if re.match(r'^(hi|hello|hey)\b', msg_lower):
            return ChatResponse(reply="Hi! 👋 I can help you understand this codebase. Ask about 'authentication', 'chat endpoint', 'database', 'security', or say 'summarize auth.py' for a full file breakdown.")

        # Check if user wants a file summary
        if msg_lower.startswith('summarize'):
            filename_match = re.search(r'summarize\s+([\w\.]+)', msg_lower)
            if filename_match:
                filename = filename_match.group(1)
                base = Path(__file__).resolve().parents[1]
                for f in base.rglob(filename):
                    try:
                        content = f.read_text(encoding='utf-8', errors='ignore')
                        lines = content.splitlines()
                        summary = f"{f.name}:\\n"
                        summary += f"Lines: {len(lines)}\\n"
                        summary += f"\\nFirst 20 lines:\\n"
                        summary += '\\n'.join(lines[:20])
                        if len(lines) > 20:
                            summary += f"\\n... ({len(lines) - 20} more lines)"
                        return ChatResponse(reply=summary)
                    except Exception:
                        pass
                return ChatResponse(reply=f"Could not find or read file '{filename}'. Try 'summarize auth.py' or 'summarize main.py'.")

        base = Path(__file__).resolve().parents[1]
        exts = {'.py', '.md', '.txt', '.json', '.yaml', '.yml', '.html'}
        keywords = set(re.findall(r"[a-zA-Z_]+", msg_lower))
        scores = {}
        snippets = {}
        for f in base.rglob('*'):
            if f.suffix.lower() not in exts:
                continue
            try:
                text = f.read_text(encoding='utf-8', errors='ignore').lower()
            except Exception:
                continue
            score = 0
            for kw in keywords:
                score += text.count(kw)
            if score:
                scores[f] = score
                # capture first matching line for context
                for line in text.splitlines():
                    for kw in keywords:
                        if kw in line:
                            snippets[f] = line.strip()[:300]
                            break
                    else:
                        continue
                    break
        if not scores:
            reply = "I couldn't find matches in the backend source.\\nTry:\\n- 'How does authentication work?'\\n- 'Summarize auth.py'\\n- 'What is the chat endpoint?'\\n- 'Explain database schema'"
            return ChatResponse(reply=reply)

        # build response from top matches
        top = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:5]
        parts = ["📚 **Found these relevant files:**\\n"]
        for f, sc in top:
            snip = snippets.get(f, '')
            parts.append(f"📄 **{f.name}** → {snip}")
        parts.append("\\nTry 'summarize <filename>' for a detailed breakdown.")
        return ChatResponse(reply='\\n'.join(parts))
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
