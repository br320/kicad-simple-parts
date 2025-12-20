from fastapi import APIRouter, HTTPException
from database import get_db_connection
from .models import ComponentHistory, ComponentHistoryCreate
import sqlite3

router = APIRouter(prefix="/components/{component_id}/history")

@router.post("/", response_model=ComponentHistory)
async def create_component_history(component_id: int, history: ComponentHistoryCreate):
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

@router.get("/")
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


