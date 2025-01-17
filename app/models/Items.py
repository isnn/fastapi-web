import uuid
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime
from typing import Optional
from sqlalchemy import func

# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, sa_column_kwargs={"onupdate": func.now()})
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)

# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    

# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID

class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int
