from fastapi import APIRouter, HTTPException, Depends
from crud import crud_session_info as crud
from sqlalchemy.orm import Session
import json
from database import get_db
from models import security_model
from services import security_service

router = APIRouter(
    prefix="/script/security",
    tags=["security_platform_scripts"]
)


@router.post("/update")
def update_security_script(request: security_model.Info, db: Session = Depends(get_db)) -> dict:
    identifier = "security"
    headers = request.headers if request.headers else {}
    cookies = request.cookies if request.cookies else {}
    ext = request.ext if request.ext else ""
    try:
        crud.upsert_session_info(db, identifier, headers, cookies, ext)
        return {"message": "Security info updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update security info: {str(e)}")


@router.post("/execute", response_model=security_model.Response)
def execute_security_script(request: security_model.Request,db: Session = Depends(get_db)):
    identifier = "security"
    headers = crud.get_session_info(db, identifier).headers if crud.get_session_info(db, identifier) else "{}"
    cookies = crud.get_session_info(db, identifier).cookies if crud.get_session_info(db, identifier) else "{}"
    headers = json.loads(headers)
    cookies = json.loads(cookies)
    try:
        res = security_service.change_status(request.tasks, status=request.status,headers=headers, cookies=cookies)
        response = security_model.Response(results=res)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing operation: {str(e)}")
