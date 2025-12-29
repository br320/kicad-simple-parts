from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_serializer 
from typing import Optional, TYPE_CHECKING, Any, ClassVar
from datetime import datetime

class PartBase(SQLModel):
    name: str
    category_id: int
    flags: int = Field(default=(0b111 << 29))
    description: Optional[str] = None
    value: Optional[str] = None
    datasheet: Optional[str] = None
    symbolIdStr: Optional[str] = None
    footprint: Optional[str] = None

    _FLAGS: ClassVar = {
            "exclude_from_bom": 0b1 << 31,
            "exclude_from_board": 0b1 << 30,
            "exclude_from_sim": 0b1 << 29,
            "id": 0b1 << 28,
            "name": 0b1 << 27,
            "description": 0b1 << 26,
            "value": 0b1 << 25,
            "datasheet": 0b1 << 24,
            "footprint": 0b1 << 23,
    }

    @classmethod
    def get_flag(cls, key):
        return cls._FLAGS.get(key, 0)


class Part(PartBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    revision: Optional[str] = Field(default="A1")
    lifecycle: Optional[str] = Field(default="Draft")
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
