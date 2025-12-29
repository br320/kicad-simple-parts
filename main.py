#!/usr/bin/env python3

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_db_and_tables
from parts.routes import router as part_router
from parts.routes import kicad_router as kicad_part_router
#from history.routes import router as history_router
#from mfg_info.routes import router as mfg_info_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
        title="KiCAD Simple Parts",
        description="Simple part lifecycle management",
        version="0.1.0",
        lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:8000"] for specific origin
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
            "parts": "",
            "categories": "",
    }

@app.get("/kicad/v1")
async def root():
    return {
            "parts": "",
            "categories": "",
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(part_router)
app.include_router(kicad_part_router)
# app.include_router(history_router)
# app.include_router(mfg_info_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
