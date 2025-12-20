from pydantic import BaseModel
from typing import Optional
from datetime import datetime


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
