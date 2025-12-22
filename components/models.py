from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from mfg_info.models import ManufacturerPart
    from history.models import ComponentHistory

class ComponentBase(SQLModel):
    name: str
    description: Optional[str] = None
    value: Optional[str] = None
    footprint: Optional[str] = None
    symbol: Optional[str] = None
    datasheet: Optional[str] = None
    lifecycle_state: str = "prototype"
    revision: Optional[str] = None


class Component(ComponentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    mfg_parts: list["ManufacturerPart"] = Relationship(back_populates="component")
    history: list["ComponentHistory"] = Relationship(back_populates="component")


class ComponentCreate(ComponentBase):
    pass


class ComponentRead(ComponentBase):
    id: int
    created_at: datetime
    updated_at: datetime
