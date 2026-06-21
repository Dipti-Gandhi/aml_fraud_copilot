# app/main.py
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import os

from .chain import chat
from .schemas import ChatRequest, ChatResponse
from .memory import clear_session_history
from .logger import logger

app = FastAPI(
    title="AML & Fraud Detection Co-Pilot Backend API",
    description="LangChain-powered financial compliance orchestrator supporting automated transaction tracking and screening."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    logger.info(f"Received query: '{req.message}'", extra={"session_id": req.session_id})

    result_data = chat(session_id=req.session_id, message=req.message)
    
    logger.info(f"Execution completed with status: {result_data['status']}", extra={"session_id": req.session_id})
    
    return ChatResponse(
        session_id=req.session_id,
        response=result_data["response"],
        status=result_data["status"]
    )

@app.post("/reset")
def reset_endpoint(payload: Dict[str, str]):
    session_id = payload.get("session_id")
    if not session_id:
        raise HTTPException(status_code=400, detail="Missing required 'session_id' field parameter.")
    
    clear_session_history(session_id)
    return {"message": f"Conversational context memory cleared successfully for session {session_id}."}

@app.get("/health")
def health_endpoint():
    return {
        "status": "healthy",
        "uptime": "nominal",
        "model_configuration": os.getenv("MODEL_NAME", "gpt-4o-mini")
    }
