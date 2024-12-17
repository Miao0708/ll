# app/routers/scripts.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud
from models import schemas
from ..database import get_db

router = APIRouter(
    prefix="/scripts",
    tags=["scripts"]
)

@router.get("/", response_model=List[schemas.Script])
def read_scripts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    scripts = crud.get_scripts(db, skip=skip, limit=limit)
    return scripts

@router.get("/count", response_model=int)
def get_script_count_endpoint(db: Session = Depends(get_db)):
    return crud.get_script_count(db)

@router.post("/", response_model=schemas.Script)
def create_script(script: schemas.ScriptCreate, db: Session = Depends(get_db)):
    db_script = crud.create_script(db, script)
    return db_script

@router.put("/{script_id}", response_model=schemas.Script)
def update_script(script_id: int, script: schemas.ScriptUpdate, db: Session = Depends(get_db)):
    db_script = crud.update_script(db, script_id, script)
    if db_script is None:
        raise HTTPException(status_code=404, detail="Script not found")
    return db_script

@router.get("/{script_id}", response_model=schemas.Script)
def get_script(script_id: int, db: Session = Depends(get_db)):
    db_script = crud.get_script(db, script_id)
    if db_script is None:
        raise HTTPException(status_code=404, detail="Script not found")
    return db_script
