from fastapi import APIRouter, HTTPException
from database import get_db_connection
from .models import Component, ComponentCreate

router = APIRouter(prefix="/components")

@router.post("/", response_model=Component)
async def create_component(component: ComponentCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO components (name, description, value, footprint, symbol, datasheet, lifecycle_state)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        component.name,
        component.description,
        component.value,
        component.footprint,
        component.symbol,
        component.datasheet,
        component.lifecycle_state,
    ))

    conn.commit()
    component_id = cursor.lastrowid

    cursor.execute("SELECT * FROM components WHERE id = ?", (component_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=500, detail="Failed to create component")
    return dict(row)
