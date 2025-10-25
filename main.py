from fastapi import FastAPI

from src.api.health.routes import health_router
from src.auth.routes import auth_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(health_router)
