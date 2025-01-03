from sqlalchemy.ext.asyncio import create_async_engine
from src.server.database.models import Base
from src.server.database.config import engine


async def init_db():
    """Create all database tables based on models."""
    async with engine.begin() as conn:
        # Uncomment the next line for development to reset the database:
        # await conn.run_sync(Base.metadata.drop_all)
        
        # Create all tables defined in models.py
        await conn.run_sync(Base.metadata.create_all)
        print("Database tables created successfully.")


if __name__ == "__main__":
    import asyncio

    # Run the async initialization script
    asyncio.run(init_db())