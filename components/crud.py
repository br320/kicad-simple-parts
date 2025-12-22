from sqlmodel import Session
from fastapi import HTTPException
from database import get_session
from .models import ComponentCreate, Component

def create_component(session: Session, component: ComponentCreate) -> Component:
    db_component = Component.model_validate(component)
    session.add(db_component)
    session.commit()
    session.refresh(db_component)
    return db_component