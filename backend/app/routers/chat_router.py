from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import get_current_user
from app.models import User
from app.schemas import ChatRequest, ChatResponse, ErrorResponse
from app.config import settings
import anthropic

router = APIRouter(prefix="/chat", tags=["Chat"])

# Enhanced knowledge base for competitive exams
KNOWLEDGE_BASE = {
    "upsc": {
        "subjects": ["history", "geography", "political science", "economy", "environment", "indian constitution"],
        "description": "UPSC Civil Services Exam preparation"
    },
    "ssc": {
        "subjects": ["english", "maths", "reasoning", "general awareness", "quantitative"],
        "description": "SSC CGL/CHSL/MTS exam preparation"
    },
    "nda": {
        "subjects": ["national defence academy", "general knowledge", "maths", "english", "military"],
        "description": "NDA exam preparation (National Defence Academy)"
    },
    "banking": {
        "subjects": ["banking awareness", "financial awareness", "rbi", "economy", "quantitative", "reasoning"],
        "description": "Banking exams (IBPS, SBI, RBI, NABARD)"
    }
}

@router.post("", response_model=ChatResponse, responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def chat(request: ChatRequest, current_user: User = Depends(get_current_user)):
    if not request.message.strip():
        raise HTTPException(400, detail="Message cannot be empty")
    
    msg_lower = request.message.strip().lower()
    
    # Try Anthropic API if available
    if settings.ANTHROPIC_API_KEY:
        try:
            client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            system_prompt = """You are AsifEdA, an expert AI assistant specialized in competitive exam preparation and banking knowledge.
You help students prepare for:
- UPSC (Civil Services, History, Geography, Economy, Constitution, Environment)
- SSC (CGL, CHSL, MTS - English, Maths, Reasoning, General Awareness)
- NDA (National Defence Academy - General Knowledge, Maths, English)
- Banking Exams (IBPS, SBI, RBI - Banking Awareness, Financial Awareness, Quantitative, Reasoning)

Provide:
1. Clear, concise explanations
2. Multiple examples for better understanding
3. Memory tricks and shortcuts for quick learning
4. Related concepts and connections
5. Practice tips and exam strategies

Format answers with:
- Bold headings for key concepts
- Bullet points for important facts
- Examples with real scenarios
- Quick tips for exam strategy"""
            
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=2000,
                system=system_prompt,
                messages=[{"role": "user", "content": request.message}]
            )
            reply = response.content[0].text
            return ChatResponse(reply=reply)
        except Exception as e:
            pass  # Fall back to local assistant if API fails
    
    # Local fallback assistant (works without API key)
    from pathlib import Path
    import re

    # Handle greetings
    if re.match(r'^(hi|hello|hey|namaste)\b', msg_lower):
        return ChatResponse(reply="""🎓 **Namaste! Welcome to AsifEdA - Your Competitive Exam Brain!**

I'm your AI assistant for:
✅ **UPSC** - History, Geography, Economics, Constitution, Environment
✅ **SSC** - English, Maths, Reasoning, General Awareness  
✅ **NDA** - General Knowledge, Maths, Military Strategy
✅ **Banking** - Banking Awareness, RBI, Quantitative, Reasoning

Ask me anything about:
- Exam concepts and topics
- Previous year questions
- Quick revision notes
- Memory tricks and shortcuts
- Strategy and tips

Example: "Explain GST", "What is Monetary Policy?", "Banking regulation rules", "NDA general knowledge"

What would you like to learn today?""")
    
    # Handle exam-specific queries
    exam_matched = None
    for exam_name, exam_info in KNOWLEDGE_BASE.items():
        if exam_name in msg_lower:
            exam_matched = exam_name
            break
    
    # Check if asking for help/resources
    if any(word in msg_lower for word in ["help", "resources", "what can", "prepare", "study"]):
        response = "📚 **AsifEdA - Your Competitive Exam Knowledge Brain**\n\n"
        response += "I can help you with:\n\n"
        for exam, info in KNOWLEDGE_BASE.items():
            response += f"🎯 **{exam.upper()}** - {info['description']}\n"
            response += f"   Topics: {', '.join(info['subjects'][:3])}...\n\n"
        response += "💡 **How to use me:**\n"
        response += "• Ask specific questions: 'What is Fiscal Policy?'\n"
        response += "• Request explanations: 'Explain the Indian Constitution'\n"
        response += "• Get quick notes: 'RBI functions explained simply'\n"
        response += "• Practice questions: 'Ask me 5 hard UPSC questions'\n"
        return ChatResponse(reply=response)
    
    # Comprehensive answer for any exam topic
    reply = f"""📖 **Comprehensive Analysis for: "{request.message.strip()}"**

Since AsifEdA AI is designed as your complete brain for competitive exams, here's what I would cover:

🧠 **Core Concepts:**
- Definition and fundamental principles
- Historical context and evolution
- Current applications and relevance
- Interconnections with related topics

📊 **For Quantitative Topics:**
- Formulas and mathematical approach
- Step-by-step solved examples
- Common mistakes and how to avoid them
- Quick calculation tricks

🏛️ **For UPSC:**
- Constitutional framework
- Historical significance
- Current affairs connection
- Governance implications

💼 **For Banking:**
- RBI guidelines and regulations
- Market implications
- Customer relevance
- Exam strategy tips

⚡ **Quick Revision Points:**
- Key facts to remember
- Memory aids and mnemonics
- Comparison with related concepts

🎯 **Exam Strategy:**
- How this topic appears in exams
- Likely question patterns
- Time management tips

**Note:** For detailed explanations, connect your ANTHROPIC_API_KEY for full AI responses. The system currently shows you the structure - connect the API key to get comprehensive AI-generated answers for any exam topic!

*To get full AI responses:*
```
export ANTHROPIC_API_KEY=your-key-here
docker-compose up -d
```"""
    
    return ChatResponse(reply=reply)

