from sqlmodel import Session
from fastapi import Depends, HTTPException
from database import get_session
from components.models import Component
from .models import ComponentHistoryRead


def get_component_history(component_id: int, session: Session = Depends(get_session)) -> list[ComponentHistoryRead]:
    component = session.get(Component, component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")

    return [ComponentHistoryRead.model_validate(h) for h in component.history]


