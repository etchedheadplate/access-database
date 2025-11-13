from fastapi import APIRouter

from src.api.database.routes.groups import router as groups_router
from src.api.database.routes.permissions import router as permissions_router
from src.api.database.routes.resources import router as resources_router
from src.api.database.routes.users import router as users_router

router = APIRouter()
router.include_router(users_router)
router.include_router(groups_router)
router.include_router(permissions_router)
router.include_router(resources_router)

__all__ = ["router"]
