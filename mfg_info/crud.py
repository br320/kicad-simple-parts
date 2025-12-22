from sqlmodel import Session
from fastapi import Depends, HTTPException
from components.models import Component
from database import get_session
from .models import ManufacturerPartCreate, ManufacturerPart, ManufacturerPartBase

def add_mfg_info(session: Session, mfg_info: ManufacturerPartCreate) -> ManufacturerPart:
    db_mfg_info = ManufacturerPart.model_validate(mfg_info)
    session.add(db_mfg_info)
    session.commit()
    session.refresh(db_mfg_info)
    return db_mfg_info

def get_mfg_info(component_id: int, session: Session = Depends(get_session)) -> list[ManufacturerPart]:
    component = session.get(Component, component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")

    return [ManufacturerPartBase.model_validate(m) for m in component.mfg_parts]
