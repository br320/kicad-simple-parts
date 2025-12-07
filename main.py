#!/usr/bin/env python3

from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db, get_db_connection
from models import Component, ComponentCreate



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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
