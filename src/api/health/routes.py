from fastapi import APIRouter, Depends

from src.auth.manager import current_active_user
from src.database.models import User

health_router = APIRouter()


@health_router.post("/ping")
async def send_pong():
    return {"message": "pong"}


@health_router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"{user.email} authenticated!"}
