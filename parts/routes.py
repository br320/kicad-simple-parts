from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from database import get_session
from .models import Part, PartRead, PartReadBasic,PartCreate, Category, CategoryCreate, CategoryRead, KicadPartRead, KicadPartReadBasic, KicadCategoryRead
from . import crud

API_VERSION = "v1"
router = APIRouter(prefix=f"/{API_VERSION}")
kicad_router = APIRouter(prefix=f"/kicad/{API_VERSION}")

@router.post("/", response_model=Part)
async def create_part(part: PartCreate, session: Session = Depends(get_session)) -> Part:
    return crud.create_part(part, session)


@router.post("/categories", response_model=Category)
async def create_category(category: CategoryCreate, session: Session = Depends(get_session)) -> Category:
    return crud.create_category(category, session)

@kicad_router.get("/categories.json", response_model=list[KicadCategoryRead])
async def kicad_get_categories(session: Session = Depends(get_session)) -> list[CategoryRead]:
    return crud.get_categories(session)

@router.get("/categories.json", response_model=list[CategoryRead])
async def get_categories(session: Session = Depends(get_session)) -> list[CategoryRead]:
    return crud.get_categories(session)


@kicad_router.get("/parts/category/{category_id}.json", response_model=list[KicadPartReadBasic])
async def kicad_get_parts_in_category(category_id: int, session: Session = Depends(get_session)) -> list[PartReadBasic]:
    return crud.get_parts_in_category(category_id, session)

@router.get("/parts/category/{category_id}.json", response_model=list[PartReadBasic])
async def get_parts_in_category(category_id: int, session: Session = Depends(get_session)) -> list[PartReadBasic]:
    return crud.get_parts_in_category(category_id, session)

@kicad_router.get("/parts/{part_id}.json", response_model=KicadPartRead)
async def get_detailed_part_info(part_id: int, session: Session = Depends(get_session)) -> PartRead:
    return crud.get_detailed_part_info(part_id, session)

@router.get("/parts/{part_id}.json", response_model=Part)
async def get_detailed_part_info(part_id: int, session: Session = Depends(get_session)) -> PartRead:
    return crud.get_detailed_part_info(part_id, session)
