from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ComponentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    value: Optional[str] = None
    footprint: Optional[str] = None
    symbol: Optional[str] = None
    datasheet: Optional[str] = None
    lifecycle_state: str = "prototype"


class Component(ComponentCreate):
    id: int
    created_at: datetime
    updated_at: datetime

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

class ComponentHistoryCreate(BaseModel):
    component_id: int
    revision: str
    change_message: str

class ComponentHistory(BaseModel):
    id: int
    component_id: int
    revision: str
    name: str
    description: Optional[str]
    value: Optional[str]
    footprint: Optional[str]
    symbol: Optional[str]
    datasheet: Optional[str]
    lifecycle_state: str
    change_message: str
    created_at: datetime
