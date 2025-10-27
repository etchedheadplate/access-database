from fastapi import APIRouter

from .groups import router as groups_router
from .permissions import router as permissions_router
from .resources import router as resources_router
from .users import router as users_router

router = APIRouter()
router.include_router(users_router)
router.include_router(groups_router)
router.include_router(permissions_router)
router.include_router(resources_router)

__all__ = ["router"]
