from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import ChatRequest, ChatResponse
from app.rag.chains import get_answer
from app.config import FIELD_NAMES

app = FastAPI(title="Chain-Field Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    if req.field not in FIELD_NAMES:
        raise HTTPException(400, detail=f"field must be one of {FIELD_NAMES}")
    try:
        reply = get_answer(req.field, req.message)
        return ChatResponse(reply=reply)
    except FileNotFoundError:
        raise HTTPException(
            503,
            detail="Vector index not built yet. Run in terminal: python -m app.rag.ingest",
        )
    except Exception as e:
        err_msg = str(e).lower()
        if "429" in err_msg or "quota" in err_msg or "ratelimit" in err_msg:
            raise HTTPException(
                503,
                detail="OpenAI API quota exceeded. Add billing at https://platform.openai.com",
            ) from e
        if "401" in err_msg or "invalid" in err_msg or "authentication" in err_msg or "api_key" in err_msg:
            raise HTTPException(
                503,
                detail="OpenAI API key missing or invalid. Check OPENAI_API_KEY in .env",
            ) from e
        raise HTTPException(500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}
