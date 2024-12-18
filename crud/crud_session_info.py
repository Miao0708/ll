# app/crud/crud_session_info.py  对session_info 的增删改查操作
from typing import Optional

from sqlalchemy.orm import Session
from models import data_model as models
import json


def get_session_info(db: Session, identifier: str) -> Optional[models.SessionInfo]:
    """
    查询session_info表，是否有identifier信息
    :param db:
    :param identifier:
    :return: 有记录则返回SessionInfo对象
    """
    return db.query(models.SessionInfo).filter(models.SessionInfo.identifier == identifier).first()


def create_session_info(db: Session, identifier: str, headers: dict, cookies: dict,
                        ext: str = "") -> models.SessionInfo:
    """
    创建记录，提交identifier headers cookies
    :param db:
    :param identifier:
    :param headers:
    :param cookies:
    :param ext:
    :return: 返回session_info model
    """
    headers_json = json.dumps(headers)
    cookies_json = json.dumps(cookies)
    session_info = models.SessionInfo(
        identifier=identifier,
        headers=headers_json,
        cookies=cookies_json,
        ext=ext
    )
    db.add(session_info)
    db.commit()
    db.refresh(session_info)
    return session_info


def update_session_info(db: Session, db_session_info: models.SessionInfo, headers: dict, cookies: dict,
                        ext: str = "") -> models.SessionInfo:
    db_session_info.headers = json.dumps(headers)
    db_session_info.cookies = json.dumps(cookies)
    db_session_info.ext = ext
    db.commit()
    db.refresh(db_session_info)
    return db_session_info


def upsert_session_info(db: Session, identifier: str, headers: dict, cookies: dict, ext: str = ""):
    db_session_info = get_session_info(db, identifier)
    if db_session_info:
        return update_session_info(db, db_session_info, headers, cookies, ext)
    else:
        return create_session_info(db, identifier, headers, cookies, ext)
