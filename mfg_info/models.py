from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ManufacturerPartCreate(BaseModel):
    component_id: int
    mfg: str
    mfgpn: str
    datasheet: Optional[str] = None
    is_preferred: bool = False
    notes: Optional[str] = None

class ManufacturerPart(ManufacturerPartCreate):
    id: int
    created_at: datetime
    updated_at: datetime

