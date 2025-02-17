from fastapi import APIRouter

from app.api.routes import items, utils, peserta, sumbangan

api_router = APIRouter()
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(peserta.router)
api_router.include_router(sumbangan.router)

# if settings.ENVIRONMENT == "local":
#     api_router.include_router(private.router)
