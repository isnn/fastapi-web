from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional
from sqlalchemy import func, Column, Numeric
import uuid
from decimal import Decimal
from pydantic import BaseModel
from sqlalchemy import Column, Numeric, ForeignKey

from app.models.Peserta import Peserta

class Sumbangan(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    id_peserta: uuid.UUID = Field(
        sa_column=Column(ForeignKey("peserta.id", ondelete="CASCADE"), nullable=False)
    )
    status: Optional[str] = Field(default=None, nullable=True)
    value: Decimal= Field(sa_column=Column(Numeric(15, 2))) 
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, sa_column_kwargs={"onupdate": func.now()})
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)

    # peserta: Peserta = Relationship(back_populates="sumbangan")

    #gpt
    peserta: Peserta = Relationship(back_populates="sumbangan")
    

class SumbanganStore(BaseModel): 
    id_peserta: uuid.UUID 
    value: Optional[Decimal]
    status: Optional[str] = None

    class Config:
        from_attributes = True  


class SumbanganUpdate(BaseModel): 
    value: Optional[Decimal] =None
    status: Optional[str] = None

    class Config:
        from_attributes = True  
   