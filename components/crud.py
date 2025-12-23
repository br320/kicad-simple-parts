from sqlmodel import Session, select
from fastapi import HTTPException
from database import get_session
from .models import ComponentCreate, Component

def create_component(session: Session, component: ComponentCreate) -> Component:
    db_component = Component.model_validate(component)
    session.add(db_component)
    session.commit()
    session.refresh(db_component)
    return db_component

def get_all_components(session: Session) -> list[Component]:
    statement = select(Component).order_by(Component.id)
    components = session.exec(statement).all()
    return [Component.model_validate(c) for c in components]
