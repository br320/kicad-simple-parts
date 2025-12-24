from sqlmodel import Session
from fastapi import Depends, HTTPException
from database import get_session
from components.models import Component
from .models import ComponentHistoryCreate, ComponentHistory, ComponentHistoryRead

def create_component_history(component_id: int, history: ComponentHistory, session: Session = Depends(get_session)) -> ComponentHistory:
    component = session.get(Component, component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")

    db_history = ComponentHistory(
        component_id=component_id,
        name=component.name,
        change_msg=history.change_msg,
        description=component.description,
        value=component.value,
        footprint=component.footprint,
        symbol=component.symbol,
        datasheet=component.datasheet,
        lifecycle_state=component.lifecycle_state,
        revision=history.revision,
    )
    session.add(db_history)
    session.commit()
    session.refresh(db_history)

    return db_history

def get_component_history(component_id: int, session: Session = Depends(get_session)) -> list[ComponentHistoryRead]:
    component = session.get(Component, component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")

    return [ComponentHistoryRead.model_validate(h) for h in component.history]


