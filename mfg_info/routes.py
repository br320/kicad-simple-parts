from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from database import get_session
from .models import ManufacturerPart, ManufacturerPartBase, ManufacturerPartCreate
from . import crud

router = APIRouter(prefix="/components/mfg_info")

@router.post("/", response_model=ManufacturerPart)
async def add_mfg_info(component: ManufacturerPartCreate, session: Session = Depends(get_session)) -> ManufacturerPart:
    return crud.add_mfg_info(session, component)

@router.get("/", response_model=list[ManufacturerPart])
async def get_mfg_info(component_id: int, session: Session = Depends(get_session)) -> list[ManufacturerPartBase]:
    return crud.get_mfg_info(component_id, session)
