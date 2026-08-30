import json
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel

from app.agent import ask_agent
from app.database import init_db, query_announcements


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="DingTalk Office Agent",
    version="0.1.0",
    lifespan=lifespan,
)


class ChatRequest(BaseModel):
    message: str
    employee: str

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "office agent is running",
    }


@app.get("/announcements")
def get_announcements(keyword: str | None = None):
    payload = {
        "keyword": keyword,
        "items": query_announcements(keyword),
    }

    return Response(
        content=json.dumps(payload, ensure_ascii=False),
        media_type="application/json; charset=utf-8",
    )


@app.post("/chat")
def chat(request: ChatRequest):
    answer = ask_agent(
        request.message,
        employee=request.employee,
    )


    return {"answer": answer}

