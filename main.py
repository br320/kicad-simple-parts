#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from database import init_db, get_db_connection
from models import (
        Component, ComponentCreate, 
        ComponentHistory, ComponentHistoryCreate, 
        ManufacturerPart, ManufacturerPartCreate
)
import sqlite3

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
        title="KiCAD Simple Parts",
        description="Simple component lifecycle management",
        version="0.1.0",
        lifespan=lifespan,
)

@app.get("/")
async def root():
    return {
            "message": "KiCAD Simple Parts API",
            "version": "0.1.0",
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/components", response_model=Component)
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

@app.post("/components/{component_id}/history", response_model=ComponentHistory)
async def create_component_history(component_id: int, history: ComponentHistoryCreate):
    """Create a history snapshot for a component at a specific revision."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verify component_id matches
    if history.component_id != component_id:
        conn.close()
        raise HTTPException(status_code=400, detail="component_id mismatch")
    
    # Get current component state
    cursor.execute("SELECT * FROM components WHERE id = ?", (component_id,))
    component = cursor.fetchone()
    
    if not component:
        conn.close()
        raise HTTPException(status_code=404, detail="Component not found")
    
    try:
        # Create history snapshot
        cursor.execute("""
            INSERT INTO component_history 
            (component_id, revision, name, description, value, footprint, symbol, lifecycle_state, change_message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            component_id,
            history.revision,
            component['name'],
            component['description'],
            component['value'],
            component['footprint'],
            component['symbol'],
            component['lifecycle_state'],
            history.change_message
        ))
        
        conn.commit()
        history_id = cursor.lastrowid
        
        # Fetch the created history entry
        cursor.execute("SELECT * FROM component_history WHERE id = ?", (history_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=500, detail="Failed to create history entry")
        
        return dict(row)
    
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="History entry for this revision already exists")

@app.get("/components/{component_id}/history")
async def get_component_history(component_id: int):
    """Get all history entries for a component."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verify component exists
    cursor.execute("SELECT id FROM components WHERE id = ?", (component_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Component not found")
    
    cursor.execute("""
        SELECT * FROM component_history 
        WHERE component_id = ? 
        ORDER BY created_at DESC
    """, (component_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


@app.post("/manufacturer-parts", response_model=ManufacturerPart)
async def create_manufacturer_parts(mfg_part: ManufacturerPartCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM components WHERE id = ?", (mfg_part.component_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Component not found")

    try:
        cursor.execute("""
            INSERT INTO manufacturer_parts (component_id, mfg, mfgpn, datasheet, is_preferred, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            mfg_part.component_id,
            mfg_part.mfg,
            mfg_part.mfgpn,
            mfg_part.datasheet,
            mfg_part.is_preferred,
            mfg_part.notes,
        ))

        conn.commit()
        mfg_id = cursor.lastrowid

        cursor.execute("SELECT * FROM manufacturer_parts WHERE id = ?", (mfg_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            raise HTTPException(status_code=500, detail="Failed to create component")
        return dict(row)

    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Manufacturer part number already exists")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
