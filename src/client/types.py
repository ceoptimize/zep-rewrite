from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class Message(BaseModel):
    role_type: str
    content: str
    role: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None

class Memory(BaseModel):
    messages: List[Message]
    summary: Optional[str] = None
    facts: Optional[List[Dict[str, Any]]] = None

class User(BaseModel):
    user_id: str
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    metadata: Optional[Dict[str, Any]]

class Session(BaseModel):
    session_id: str
    user_id: str
    metadata: Optional[Dict[str, Any]]