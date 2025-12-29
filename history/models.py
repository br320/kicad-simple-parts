from sqlmodel import SQLModel, Field, Relationship 
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from components.models import Component


class PartHistoryBase(SQLModel):
    message: str

class PartHistory(PartHistoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    part_id: int = Field(foreign_key="part.id")

    # Relationships
    part: "Part" = Relationship(back_populates="history")
    name: str
    description: str
    value: str
    datasheet: str
    symbolIdStr: str
    footprint: str
    revision: str 
    lifecycle: str

class PartHistoryCreate(PartHistoryBase):
    pass
