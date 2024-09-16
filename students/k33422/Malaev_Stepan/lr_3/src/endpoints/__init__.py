from fastapi import APIRouter

from .authorization import router as authorization_router
from .user import router as user_router
from .budget import router as budget_router
from .category import router as category_router
from .transaction import router as transaction_router
from .relationship import router as relationship_router
from .task import router as task_router

__all__ = ["router"]

router = APIRouter()

router.include_router(authorization_router)
router.include_router(user_router)
router.include_router(budget_router)
router.include_router(category_router)
router.include_router(transaction_router)
router.include_router(relationship_router)
router.include_router(task_router)
