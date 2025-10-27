from fastapi import APIRouter

from .add import router as add_router
from .check import router as check_router
from .remove import router as remove_router
from .view import router as view_router

router = APIRouter()
router.include_router(add_router)
router.include_router(check_router)
router.include_router(remove_router)
router.include_router(view_router)

__all__ = ["router"]
