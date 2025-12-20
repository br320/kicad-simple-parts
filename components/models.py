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
