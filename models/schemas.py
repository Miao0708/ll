# app/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class ScriptType(str, Enum):
    report = "report"
    crawl = "crawl"

class ScriptBase(BaseModel):
    name: str
    category: str
    remarks: Optional[str] = None
    type: ScriptType

class ScriptCreate(ScriptBase):
    pass

class ScriptUpdate(BaseModel):
    remarks: Optional[str] = None

class Script(ScriptBase):
    id: int

    class Config:
        orm_mode = True

# 请求和响应模型
class ReportDataRequest(BaseModel):
    creative_id: int
    n_days: Optional[int] = None
    operation_type: Optional[str] = None  # "generate" 或 "delete"

class CrawlDataRequest(BaseModel):
    headers: dict
    start_date: str  # 格式: YYYY-MM-DD
    end_date: str    # 格式: YYYY-MM-DD
