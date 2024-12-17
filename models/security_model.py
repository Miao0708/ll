from typing import Optional, Dict, Any

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text
from database import Base


class Request(BaseModel):
    tasks: list[int]
    status: int


class Result(BaseModel):
    success: int
    failed: int


class TaskResult(BaseModel):
    task_id: int
    result: Result


class Response(BaseModel):
    results: list[TaskResult]


class Infos(BaseModel):
    headers: Optional[Dict[str, Any]] = None
    cookies: Optional[Dict[str, Any]] = None
    ext: Optional[str] = None

# class ErrorResponse(BaseModel):
#     error: str
