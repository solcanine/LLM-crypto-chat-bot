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
    except FileNotFoundError as e:
        raise HTTPException(
            503,
            detail="Vector index not built yet. Run in terminal: python -m app.rag.ingest",
        ) from e
    except Exception as e:
        raise HTTPException(500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}
