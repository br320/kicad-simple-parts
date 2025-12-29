from sqlmodel import Session, select
from fastapi import HTTPException
from database import get_session
from .models import (
        Part, 
        PartCreate, 
        PartRead, 
        PartUpdate, 
        PartReadBasic, 
        CategoryCreate, 
        Category, 
        CategoryRead
    )
from history.crud import save_snapshot

def _update_rev(rev: str, prod: bool) -> str:
    a = ''.join(list(filter(lambda x: x.isalpha(), rev)))
    if prod:
        return chr(((ord(a) - ord('A')) + 1) % 26 + ord('A'))
    n = list(filter(lambda x: x.isdigit(), rev))
    if len(n) < 1: # previously production rev
        a = chr(((ord(a) - ord('A')) + 1) % 26 + ord('A'))
        n = "1"
    else:
        n = ''.join(list(filter(lambda x: x.isdigit(), rev)))
        n = str(int(n) + 1)
    rev = a + n
    return rev

def create_part(part: PartCreate, session: Session) -> Part:
    db_part = Part.model_validate(part)
    session.add(db_part)
    session.commit()
    session.refresh(db_part)
    save_snapshot(db_part.id, part.message, session)
    return db_part

def update_part(part_id: int, update: PartUpdate, session: Session) -> Part:
    part = session.get(Part, part_id)
    if not part:
        raise HTTPException(status_code=404, detail=f"Part-{part_id} not found")
    keys = update.model_dump(exclude_unset=True).keys()
    if "revision" not in keys:
        lifecycle = getattr(update, "lifecycle", None)
        prod = part.lifecycle == "Production" if not lifecycle else lifecycle == "Production"
        part.revision = _update_rev(part.revision, prod)
    for key in keys:
        if key == "message":
            continue
        val = getattr(update, key, None)
        assert val
        setattr(part, key, val)
    session.add(part)
    session.commit()
    session.refresh(part)
    save_snapshot(part.id, update.message, session)
    return part

def get_detailed_part_info(part_id: int, session: Session) -> PartRead:
    part = session.get(Part, part_id).model_dump()
    if not part:
        raise HTTPException(status_code=404, detail=f"Part-{part_id} not found")
    part_read = PartRead.model_validate(part)
    part_read.exclude_from_bom = part["flags"] & Part.get_flag("exclude_from_bom") != 0
    part_read.exclude_from_board = part["flags"] & Part.get_flag("exclude_from_board") != 0
    part_read.exclude_from_sim = part["flags"] & Part.get_flag("exclude_from_sim") != 0
    for key in part.keys():
        if key not in part_read.model_dump().keys() and key != "flags":
            visible = (part["flags"] & Part.get_flag(key)) != 0
            part_read.fields[key] = { 
                "value": str(part[key]),
                "visible": str(visible)
            }
    return part_read

def get_categories(session: Session) -> list[CategoryRead]:
    statement = select(Category).order_by(Category.id)
    categories = session.exec(statement).all()
    return [CategoryRead.model_validate(category) for category in categories]

def get_parts_in_category(category_id: int, session: Session) -> list[PartReadBasic]:
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail=f"Category-{part_id} not found")
    statement = select(Part).where(Part.category_id == category_id)
    parts = session.exec(statement).all()
    return [PartReadBasic.model_validate(part) for part in parts]

def create_category(category: CategoryCreate, session: Session) -> Category:
    db_category = Category.model_validate(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category
