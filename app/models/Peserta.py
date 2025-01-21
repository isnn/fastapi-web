from sqlmodel import Field, Relationship, SQLModel
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from sqlalchemy import func
import uuid
from decimal import Decimal
from enum import Enum

class DayEnums(str, Enum):
    senin = "senin"
    selasa = "selasa"
    rabu = "rabu"
    kamis = "kamis"
    jumat = "jumat"
    sabtu = "sabtu"
    minggu = "minggu"

class Peserta(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    nama: str = Field(default=None)
    shift:  Optional[str]  = Field(default=None, nullable=True)
    shift_kebersihan:  Optional[str]  = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, sa_column_kwargs={"onupdate": func.now()})
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)


class PesertaStore(BaseModel):
    nama: str
    shift: Optional[DayEnums] = None  # Optional field, default None
    shift_kebersihan: Optional[DayEnums] = None  # Optional field, default None

    class Config:
        from_attributes = True  
