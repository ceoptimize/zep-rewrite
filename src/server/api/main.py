from fastapi import FastAPI, HTTPException, Depends
from typing import List
from ...client.types import Message, Memory, User, Session
from ..database.models import SessionDB, UserDB, MessageDB
from ..database.config import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Welcome to the API!"}

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

# @app.get("/api/v1/memory/{session_id}")
# async def get_memory(session_id: str, db: AsyncSession = Depends(get_db)) -> Memory:
#     messages = await db.query(MessageDB).filter(MessageDB.session_id == session_id).all()
#     return Memory(messages=[Message(**msg.dict()) for msg in messages])

@app.get("/api/v1/memory/{session_id}")
async def get_memory(session_id: str, db: AsyncSession = Depends(get_db)) -> Memory:
    # Use `select` to query the database
    stmt = select(MessageDB).filter(MessageDB.session_id == session_id)
    result = await db.execute(stmt)  # Execute the query
    messages = result.scalars().all()  # Get the result as a list

    if not messages:
        raise HTTPException(status_code=404, detail="No messages found for the given session ID")

    return Memory(messages=[Message(**msg.__dict__) for msg in messages])

@app.get("/api/v1/users/{user_id}")
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)) -> User:
    stmt = select(UserDB).filter(UserDB.user_id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalars().first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return User(**db_user.__dict__)