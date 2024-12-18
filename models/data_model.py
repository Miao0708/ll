# ./models/data_model.py  数据库模型

from sqlalchemy import Column, Integer, String, Text
from database import Base


class SessionInfo(Base):
    __tablename__ = "session_info"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    identifier = Column(String(50), unique=True, index=True, nullable=False, default="")
    headers = Column(Text, nullable=True, default="")
    cookies = Column(Text, nullable=True, default="")
    ext = Column(Text, nullable=True, default="")
