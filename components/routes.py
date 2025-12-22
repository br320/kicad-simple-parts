from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from database import get_session
from .models import Component, ComponentCreate
from . import crud

router = APIRouter(prefix="/components")

@router.post("/", response_model=Component)
async def create_component(component: ComponentCreate, session: Session = Depends(get_session)) -> Component:
    return crud.create_component(session, component)
