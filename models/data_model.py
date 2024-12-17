# app/models.py

from sqlalchemy import Column, Integer, String, Text
from database import Base

class SessionMessages(Base):
    __tablename__ = "session_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    idf = Column(String(50), unique=True, index=True, nullable=False, default="")
    headers = Column(Text, nullable=True, default="")
    cookies = Column(Text, nullable=True, default="")
    ext = Column(Text, nullable=True, default="")
