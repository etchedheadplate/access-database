from fastapi import APIRouter

from .accesses import router as accesses_router
from .groups import router as groups_router
from .resources import router as resources_router
from .users import router as users_router

router = APIRouter()
router.include_router(users_router)
router.include_router(groups_router)
router.include_router(accesses_router)
router.include_router(resources_router)

__all__ = ["router"]
