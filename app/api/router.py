from fastapi import APIRouter

from app.api.routes import admin, transaction, user, halte


api_router = APIRouter(prefix="/api")
api_router.include_router(user.router)
api_router.include_router(transaction.router)
api_router.include_router(admin.router)
api_router.include_router(halte.router)
