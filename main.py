#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from database import init_db
from components.routes import router as component_route
from history.routes import router as history_route
from mfg_info.routes import router as mfg_info_route

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

app.include_router(component_route)
app.include_router(history_route)
app.include_router(mfg_info_route)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
