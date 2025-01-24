import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import SessionDep
from app.models.Peserta import Peserta, PesertaStore, PesertaUpdate
from app.models.Sumbangan import Sumbangan, SumbanganStore, SumbanganUpdate
from app.requests.GeneralRequest import Message
from fastapi import Request

from app.core.helper.apiresponse import *

from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/sumbangan", tags=["sumbangan"])

@router.get("/")
def get_sumbangan(db: SessionDep, offset: int = 0, limit: int = 100):
    pesertas = db.exec(select(Sumbangan).offset(offset).limit(limit)).all()
    return success_response(pesertas)


@router.get("/{id}")
def get_sumbangan(db: SessionDep, id: uuid.UUID):

    sumbangan = db.exec(
        select(Sumbangan)
        .options(selectinload(Sumbangan.peserta))
        .where(Sumbangan.id == id)
    ).first()

    return success_response(sumbangan)

@router.post("/")
def create_sumbangan(db: SessionDep, request: SumbanganStore ):
    print(request)
    sumbangan = Sumbangan(
        id_peserta=request.id_peserta,
        value=request.value,
        status=request.status
    )
    db.add(sumbangan)
    db.commit()
    db.refresh(sumbangan)
    print(sumbangan)
    return success_response(sumbangan)

@router.put("/{id}")
def update_sumbangan(db: SessionDep, id: uuid.UUID, request:SumbanganUpdate ):
    sumbangan = db.get(Sumbangan, id)
    update_dict = request.model_dump(exclude_unset=True)
    sumbangan.sqlmodel_update(update_dict)
    db.add(sumbangan)
    db.commit()
    db.refresh(sumbangan)
    return success_response(sumbangan)


@router.delete("/{id}")
def delete_sumbangan(db: SessionDep, id: uuid.UUID):
    sumbangan = db.get(Sumbangan, id)

    if not sumbangan:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(sumbangan)
    db.commit()
    return Message(message="Sumbangan deleted successfully")
