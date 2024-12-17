# app/routers/script_details.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import schemas
from ..database import get_db

router = APIRouter(
    prefix="/script_details",
    tags=["script_details"]
)

@router.post("/report/generate_data")
def generate_report_data(request: schemas.ReportDataRequest, db: Session = Depends(get_db)):
    # 示例：打印接收到的参数
    print(f"Generating report data for creative_id: {request.creative_id}, n_days: {request.n_days}")
    return {"message": "Report data generation started."}

@router.post("/report/manage_order")
def manage_order_data(request: schemas.ReportDataRequest, db: Session = Depends(get_db)):
    if request.operation_type == "generate":
        print(f"Generating order data for creative_id: {request.creative_id}")
        return {"message": "Order data generation started."}
    elif request.operation_type == "delete":
        print(f"Deleting order data for creative_id: {request.creative_id}")
        return {"message": "Order data deletion started."}
    else:
        raise HTTPException(status_code=400, detail="Invalid operation type.")

@router.post("/crawl/download_excel")
def download_crawl_data(request: schemas.CrawlDataRequest, db: Session = Depends(get_db)):
    print(f"Downloading crawl data with headers: {request.headers}, from {request.start_date} to {request.end_date}")
    # 模拟下载excel文件
    return {"message": "Crawl data download started."}
