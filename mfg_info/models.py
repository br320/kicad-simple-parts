from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from components.models import ManufacturerPart


class ManufacturerPartBase(SQLModel):
    component_id: int = Field(foreign_key="component.id")
    mfg: str
    mfgpn: str
    datasheet: Optional[str] = None
    is_preferred: bool = False
    notes: Optional[str] = None

class ManufacturerPart(ManufacturerPartBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    component: "Component" = Relationship(back_populates="mfg_parts")

class ManufacturerPartCreate(ManufacturerPartBase):
    pass
