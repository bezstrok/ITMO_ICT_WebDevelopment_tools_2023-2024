from fastapi import APIRouter

from .authorization import router as authorization_router

__all__ = ["router"]

router = APIRouter()

router.include_router(authorization_router)
