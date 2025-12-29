from sqlmodel import Session
from fastapi import Depends, HTTPException
from database import get_session
from parts.models import Part
from .models import PartHistoryCreate, PartHistory


"""
def get_component_history(component_id: int, session: Session = Depends(get_session)) -> list[ComponentHistoryRead]:
    component = session.get(Component, component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")

    return [ComponentHistoryRead.model_validate(h) for h in component.history]
"""


def save_snapshot(part_id: int, message: str, session: Session = Depends(get_session)) -> PartHistory:
    part = session.get(Part, part_id)
    if not part:
        raise HTTPException(status_code=404, detail=f"Part-{part_id} not found")
    db_history = PartHistory(
        part_id = part_id,
        message = message,
        name = part.name, 
        description = part.description,
        value = part.value,
        datasheet = part.datasheet,
        symbolIdStr = part.symbolIdStr,
        footprint = part.footprint,
        revision = part.revision,
        lifecycle = part.lifecycle,
    )
    session.add(db_history)
    session.commit()
    session.refresh(db_history)
    
