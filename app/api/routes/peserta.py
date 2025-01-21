import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import SessionDep
from app.models.Peserta import Peserta, PesertaStore
from app.requests.GeneralRequest import Message

from app.core.helper.apiresponse import *

router = APIRouter(prefix="/peserta", tags=["peserta"])

# Example route that triggers a 400 error (Bad Request)
@router.get("/trigger")
async def trigger_error():
    print('skskskkssksssssssssssssssssssssssssssssssssssssssssssssss')

@router.get("/")
def get_pesertas(db: SessionDep, offset: int = 0, limit: int = 100):
    pesertas = db.exec(select(Peserta).offset(offset).limit(limit)).all()
    return success_response(pesertas)

# @router.get("/{id}")
# def detail_peserta(db: SessionDep, id: uuid.UUID):
#     peserta = db.get(Peserta, id)   
#     # return peserta
#     return success_response(peserta)

@router.post("/")
def create_peserta(db: SessionDep, request: PesertaStore ):
    peserta = Peserta(
        nama=request.nama,
        shift=request.shift,  # Optional, default 'None' will be used if not passed
        shift_kebersihan=request.shift_kebersihan,  # Optional, default 'None' will be used
    )
    db.add(peserta)
    db.commit()
    db.refresh(peserta)
    return success_response(peserta)
    # return peserta

