# app/crud_session_message.py

from sqlalchemy.orm import Session
from models import data_model as models
import json

def get_session_message(db: Session, identifier: str = "security"):
    return db.query(models.SessionMessages).filter(models.SessionMessages.identifier == identifier).first()

def create_session_message(db: Session, identifier: str, headers: dict, cookies: dict, ext: str = ""):
    headers_json = json.dumps(headers)
    cookies_json = json.dumps(cookies)
    session_message = models.SessionMessages(
        identifier=identifier,
        headers=headers_json,
        cookies=cookies_json,
        ext=ext
    )
    db.add(session_message)
    db.commit()
    db.refresh(session_message)
    return session_message

def update_session_message(db: Session, db_session_message: models.SessionMessages, headers: dict, cookies: dict, ext: str = ""):
    db_session_message.headers = json.dumps(headers)
    db_session_message.cookies = json.dumps(cookies)
    db_session_message.ext = ext
    db.commit()
    db.refresh(db_session_message)
    return db_session_message

def upsert_session_message(db: Session, identifier: str, headers: dict, cookies: dict, ext: str = ""):
    db_session_message = get_session_message(db, identifier)
    if db_session_message:
        return update_session_message(db, db_session_message, headers, cookies, ext)
    else:
        return create_session_message(db, identifier, headers, cookies, ext)
