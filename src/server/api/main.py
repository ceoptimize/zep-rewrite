from fastapi import FastAPI, HTTPException, Depends
from typing import List
from ...client.types import Message, Memory, User, Session
from ..database.models import SessionDB, UserDB, MessageDB
from ..database.config import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

# Dependency to get database session
async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

@app.post("/api/v1/users")
async def create_user(user: User, db: AsyncSession = Depends(get_db)):
    db_user = UserDB(**user.dict())
    db.add(db_user)
    await db.commit()
    return user

@app.post("/api/v1/sessions")
async def create_session(session: Session, db: AsyncSession = Depends(get_db)):
    db_session = SessionDB(**session.dict())
    db.add(db_session)
    await db.commit()
    return session

@app.post("/api/v1/memory/{session_id}")
async def add_memory(session_id: str, messages: List[Message], db: AsyncSession = Depends(get_db)):
    db_messages = [MessageDB(**msg.dict(), session_id=session_id) for msg in messages]
    db.add_all(db_messages)
    await db.commit()
    return {"status": "success"}

@app.get("/api/v1/memory/{session_id}")
async def get_memory(session_id: str, db: AsyncSession = Depends(get_db)) -> Memory:
    messages = await db.query(MessageDB).filter(MessageDB.session_id == session_id).all()
    return Memory(messages=[Message(**msg.dict()) for msg in messages])