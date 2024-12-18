from typing import Optional, Dict, Any

from pydantic import BaseModel


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


class Info(BaseModel):
    """
    更新headers  cookies 请求封装
    """
    headers: Optional[Dict[str, Any]]
    cookies: Optional[Dict[str, Any]]
    ext: Optional[Dict[str, Any]]={}


# class ErrorResponse(BaseModel):
#     error: str
