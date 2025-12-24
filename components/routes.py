from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from database import get_session
from .models import Component, ComponentCreate
from . import crud

router = APIRouter(prefix="/components")

@router.post("/", response_model=Component)
async def create_component(component: ComponentCreate, session: Session = Depends(get_session)) -> Component:
    return crud.create_component(session, component)

@router.get("/", response_model=list[Component])
async def get_all_components(session: Session = Depends(get_session)) -> list[Component]:
    return crud.get_all_components(session)

@router.get("/{component_id}", response_model=Component)
async def get_component(component_id: int, session: Session = Depends(get_session)) -> Component:
    return crud.get_components(component_id, session)

@router.put("/{component_id}", response_model=Component)
async def update_component(component_id: int, component: ComponentCreate, session: Session = Depends(get_session)) -> Component:
    return crud.update_component(component_id, session, component)

@router.delete("/{component_id}", response_model=Component)
async def delete_component(component_id: int, session: Session = Depends(get_session)):
    return ...
