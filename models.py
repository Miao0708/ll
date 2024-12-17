# app/models.py
from sqlalchemy import Column, Integer, String, Enum
from .database import Base
import enum


class ScriptType(enum.Enum):
    report = "report"
    crawl = "crawl"


class Script(Base):
    __tablename__ = "scripts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, nullable=False)
    remarks = Column(String, nullable=True)
    type = Column(Enum(ScriptType), nullable=False)
