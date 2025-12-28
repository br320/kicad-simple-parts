from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_serializer
from typing import Optional, TYPE_CHECKING, Any
from datetime import datetime

class PartBase(SQLModel):
    name: str
    category_id: int
    description: Optional[str] = None
    value: Optional[str] = None
    datasheet: Optional[str] = None
    symbolIdStr: Optional[str] = None
    footprint: Optional[str] = None


class Part(PartBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PartCreate(PartBase):
    pass

class PartRead(SQLModel):
    id: int
    name: str
    description: str
    symbolIdStr: str
    exclude_from_bom: bool = False
    exclude_from_board: bool = False
    exclude_from_sim: bool = False
    fields: Optional[dict[str, Any]] = {}

class PartReadBasic(SQLModel):
    id: int
    name: str
    description: str

class CategoryBase(SQLModel):
    name: str
    description: str

class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int

class KicadPartRead(PartRead):
    @field_serializer("*")
    def stringify(self, v, info):
        if info.field_name == "fields":
            return v
        return str(v)

class KicadPartReadBasic(PartReadBasic):
    @field_serializer("*")
    def stringify(self, v):
        return str(v)

class KicadCategoryRead(CategoryRead):
    @field_serializer("*")
    def stringify(self, v):
        return str(v)
