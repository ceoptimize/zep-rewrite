from typing import Optional, List, Dict, Any
import httpx
from .types import Message, Memory, User, Session

class AsyncMemoryClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        self.client = httpx.AsyncClient(base_url=base_url, headers=self.headers)

    async def add_memory(self, session_id: str, messages: List[Message]) -> None:
        response = await self.client.post(
            f"/api/v1/memory/{session_id}",
            json=[msg.dict() for msg in messages]
        )
        response.raise_for_status()
        return response.json()

    async def get_memory(self, session_id: str) -> Memory:
        response = await self.client.get(f"/api/v1/memory/{session_id}")
        response.raise_for_status()
        return Memory(**response.json())

class AsyncClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.memory = AsyncMemoryClient(base_url, api_key)
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        self.client = httpx.AsyncClient(base_url=base_url, headers=self.headers)

    async def create_user(self, user: User) -> User:
        response = await self.client.post("/api/v1/users", json=user.dict())
        response.raise_for_status()
        return User(**response.json())

    async def create_session(self, session: Session) -> Session:
        response = await self.client.post("/api/v1/sessions", json=session.dict())
        response.raise_for_status()
        return Session(**response.json())