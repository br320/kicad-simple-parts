from sqlmodel import SQLModel, Field, Relationship 
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from components.models import Component


class ComponentHistoryBase(SQLModel):
    component_id: int = Field(foreign_key="component.id")
    name: str
    change_msg: str
    lifecycle_state: str = "prototype"
    description: Optional[str] = None
    value: Optional[str] = None
    footprint: Optional[str] = None
    symbol: Optional[str] = None
    datasheet: Optional[str] = None
    revision: Optional[str] = None

class ComponentHistory(ComponentHistoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    component: "Component" = Relationship(back_populates="history")

class ComponentHistoryCreate(ComponentHistoryBase):
    pass

class ComponentHistoryRead(ComponentHistoryBase):
    id: int
    created_at: datetime
