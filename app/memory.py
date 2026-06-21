# app/memory.py
from typing import Dict
from langchain_community.chat_message_histories import ChatMessageHistory

_session_registry: Dict[str, ChatMessageHistory] = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in _session_registry:
        _session_registry[session_id] = ChatMessageHistory()
    return _session_registry[session_id]

def clear_session_history(session_id: str) -> None:
    if session_id in _session_registry:
        _session_registry[session_id].clear()
