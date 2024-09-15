from fastapi import APIRouter

from .authorization import router as authorization_router
from .user import router as user_router
from .budget import router as budget_router
from .category import router as category_router

__all__ = ["router"]

router = APIRouter()

router.include_router(authorization_router)
router.include_router(user_router)
router.include_router(budget_router)
router.include_router(category_router)
