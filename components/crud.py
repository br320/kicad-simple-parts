from sqlmodel import Session, select
from fastapi import HTTPException
from database import get_session
from .models import ComponentCreate, Component
from history.models import ComponentHistory

def create_component(session: Session, component: ComponentCreate) -> Component:
    db_component = Component.model_validate(component)
    session.add(db_component)
    session.commit()
    session.refresh(db_component)

    db_history = ComponentHistory(
        component_id=db_component.id,
        name=db_component.name,
        change_msg="initial release",
        description=db_component.description,
        value=db_component.value,
        footprint=db_component.footprint,
        symbol=db_component.symbol,
        datasheet=db_component.datasheet,
        lifecycle_state=db_component.lifecycle_state,
        revision=db_component.revision,
    )
    session.add(db_history)
    session.commit()
    session.refresh(db_history)
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
    db_component = Component.model_validate(component)
    original = session.get(Component, component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")

    original.name = component.name
    original.description = component.description
    original.value = component.value
    original.datasheet = component.datasheet
    original.footprint = component.footprint
    original.symbol = component.symbol
    original.revision = component.revision
    original.lifecycle_state = component.lifecycle_state

    db_history = ComponentHistory(
        component_id=component_id,
        name=original.name,
        change_msg="<sample change msg>",
        description=original.description,
        value=original.value,
        footprint=original.footprint,
        symbol=original.symbol,
        datasheet=original.datasheet,
        lifecycle_state=original.lifecycle_state,
        revision=original.revision,
    )

    session.add(original)
    session.add(db_history)
    session.commit()
    session.refresh(original)
    session.refresh(db_history)
    return original
