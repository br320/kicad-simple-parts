from fastapi import APIRouter, HTTPException
from database import get_db_connection
from .models import ManufacturerPart, ManufacturerPartCreate
import sqlite3

router = APIRouter(prefix="/manufacturer-parts")

@router.post("/", response_model=ManufacturerPart)
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

