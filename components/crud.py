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

def get_components(component_id: int, session: Session) -> Component:
    component = session.get(Component, component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    return component

def update_component(component_id: int, session: Session, component: ComponentCreate) -> Component:
    original = session.get(Component, component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    db_component = Component.model_validate(component)
    original.name = component.name
    original.description = component.description
    original.value = component.value
    original.datasheet = component.datasheet
    original.footprint = component.footprint
    original.symbol = component.symbol
    original.revision = component.revision
    original.lifecycle_state = component.lifecycle_state

    session.add(original)
    session.commit()
    session.refresh(original)
    return original
