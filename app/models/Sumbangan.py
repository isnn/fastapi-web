from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime
from typing import Optional
from sqlalchemy import func, Column, Numeric
import uuid
from decimal import Decimal

class Sumbangan(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    id_peserta: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    status: str = Field(default='None')
    value: Decimal= Field(sa_column=Column(Numeric(15, 2))) 
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, sa_column_kwargs={"onupdate": func.now()})
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)
