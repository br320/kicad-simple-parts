from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from database import get_session
from .models import ComponentHistory, ComponentHistoryCreate, ComponentHistoryRead
from . import crud

router = APIRouter(prefix="/components/{component_id}/history")

@router.post("/", response_model=ComponentHistoryCreate)
async def create_component_history(component_id: int, history: ComponentHistoryCreate, session: Session = Depends(get_session)) -> ComponentHistoryCreate:
    return crud.create_component_history(component_id, history, session)

@router.get("/", response_model=list[ComponentHistoryRead])
async def get_component_history(component_id: int, session: Session = Depends(get_session)) -> list[ComponentHistoryRead]:
    return crud.get_component_history(component_id, session)
