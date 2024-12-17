from fastapi import APIRouter, HTTPException, Depends
from typing import List
from crud import crud_session_message as crud
from sqlalchemy.orm import Session

from database import get_db
from models import security_model
from services import security_service
router = APIRouter(
    prefix="/security",
    tags=["security_platform_scripts"]
)
#
headers = {
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Authorization": "Bearer eyJhbGciOiJIUzUxMiIsInppcCI6IkRFRiJ9.eNqqVsoqyVSyUspPLC3JCMnPTs1T0lEqLk0CCkXoOgYE6Aa7BoW5BgEFM4uLgYIpqWXFqcn5BcW6JSDFusWpRWWpRSDpxBIlK0NzYxNjS0tzA3MdpVKgVFB-TipQV3Q1mOeZomRlZmhmbKajVASUAHGNIUzn_JRUoOHBrs7x7q5-rkGOPvGhwWBbQbJ-ibkg2Wcz171smPV8yopnHduVamMhNjgmJ-eX5gGtVsrJz0vPzUzMV4JIQDW96J7-ct9MqBjcAbUAAAAA__8.abXyHWJLFPrQBV-_RUTVjHP9Fc-sIGnxCX8M0syHp9II5ixrhUrvXAQ7om7EN3hE4jKIjIZ6Uc4rhhIwCedb8g",
    "Cache-Control": "no-cache",
    "Host": "isec.iflytek.com",
    "Origin": "https://isec.iflytek.com",
    "Pragma": "no-cache",
    "Referer": "https://isec.iflytek.com/sdl/detect/code/detail/121808?taskStatus=1&taskType=SEC_CODE&scannerType=1",
    "Sec-CH-UA": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
cookies = {
    "tmr_lvid": "daf9e2f2e26cee3ae8dbeee74c64b8a1",
    "tmr_lvidTS": "1722837884778",
    "_gcl_au": "1.1.1591203014.1730790907",
    "_ga": "GA1.2.315748175.1730790908",
    "_ga_VPYRHN104D": "GS1.1.1730790907.1.1.1730791474.60.0.0",
    "__tea__ug__uid": "8971661730791475546",
    "casgwusercred": "fXXQtH5PW3YmTk9UI5pOnICiSl9eJQQYIHQ8S7RnkQY_PJbOq-ehc99H7bet-hqyKMv1WHdruxpWEYLD1_yc49tyYeorZOCZ4rV6jBqoMO5LV8xzGKDI9kWHgMSPWN8xY9KRdpy6OXk6_rZV1EeMUfwMUjaf3rE34H4-azz2T9Y",
    "crosgwusercred": "VbhNbXW3HKRlWaID374UhELrta6FwuubdVClefov3X139Lo6T7RDxYk3g0ZjR85GdRVhtu9bbz68CHPFUsxZUQd94fa158c82a8eeecc1571d7b6bb5e92"
}
@router.post("/update")
def update_security_script(request: security_model.Infos,db: Session = Depends(get_db)):
    identifier = "security"
    headers = request.headers if request.headers else {}
    cookies = request.cookies if request.cookies else {}
    ext = request.ext if request.ext else ""
    try:
        crud.upsert_session_message(db, identifier, headers, cookies, ext)
        return {"message": "Security info updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update security info: {str(e)}")

@router.post("/execute", response_model=security_model.Response)
def execute_security_script(request: security_model.Request):
    try:
        res = security_service.change_status(request.tasks, request.status)
        response = security_model.Response(results=res)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing operation: {str(e)}")
