import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import SessionDep
from app.models.Peserta import Peserta, PesertaStore, PesertaUpdate, PesertaExpand
from app.requests.GeneralRequest import Message

from app.core.helper.apiresponse import *
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/peserta", tags=["peserta"])

@router.get("/")
def get_pesertas(db: SessionDep, offset: int = 0, limit: int = 100):
    pesertas = db.exec(select(Peserta).offset(offset).limit(limit)).all()
    return success_response(pesertas)

@router.get("/{id}", response_model=PesertaExpand)
def detail_peserta(db: SessionDep, id: uuid.UUID):
    peserta = (
        db.exec(
            select(Peserta)
            .where(Peserta.id == id)
            .options(selectinload(Peserta.sumbangan))  # Load relationship
        )
    ).first()
    return peserta

@router.post("/")
def create_peserta(db: SessionDep, request: PesertaStore ):
    peserta = Peserta(
        nama=request.nama,
        shift=request.shift,  
        shift_kebersihan=request.shift_kebersihan,
    )
    db.add(peserta)
    db.commit()
    db.refresh(peserta)
    return success_response(peserta)

@router.put("/{id}")
def update_peserta(db: SessionDep, id: uuid.UUID, request: PesertaUpdate ):
    peserta = db.get(Peserta, id)  
    update_dict = request.model_dump(exclude_unset=True)
    peserta.sqlmodel_update(update_dict)
    db.add(peserta)
    db.commit()
    db.refresh(peserta)
    return peserta

@router.delete("/{id}")
def delete_peserta(db: SessionDep, id: uuid.UUID):
    peserta = db.get(Peserta, id)

    if not peserta:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(peserta)
    db.commit()
    return Message(message="Item deleted successfully")
