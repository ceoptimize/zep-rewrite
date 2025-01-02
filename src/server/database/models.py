from sqlalchemy import Column, String, JSON, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"
    
    user_id = Column(String, primary_key=True)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    meta_data = Column(JSON)  # Changed from metadata to meta_data
    created_at = Column(DateTime, default=datetime.utcnow)

class SessionDB(Base):
    __tablename__ = "sessions"
    
    session_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    meta_data = Column(JSON)  # Changed from metadata to meta_data
    created_at = Column(DateTime, default=datetime.utcnow)

class MessageDB(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True)
    session_id = Column(String, ForeignKey("sessions.session_id"))
    role_type = Column(String)
    content = Column(String)
    role = Column(String)
    meta_data = Column(JSON)  # Changed from metadata to meta_data
    created_at = Column(DateTime, default=datetime.utcnow)