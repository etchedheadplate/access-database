from fastapi import APIRouter

from src.api.access.routes.add import router as grant_router
from src.api.access.routes.check import router as check_router
from src.api.access.routes.remove import router as remove_router
from src.api.access.routes.view import router as view_router

router = APIRouter()
router.include_router(grant_router)
router.include_router(check_router)
router.include_router(remove_router)
router.include_router(view_router)

__all__ = ["router"]
