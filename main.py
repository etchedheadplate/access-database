from fastapi import FastAPI

from src.api.access.routes import router as access_router
from src.api.auth.routes import router as auth_router
from src.api.database.routes import router as database_router
from src.api.health.routes import router as health_router

app = FastAPI()
app.include_router(health_router, tags=["Health"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(database_router, prefix="/database", tags=["Database"])
app.include_router(access_router, prefix="/access", tags=["Access"])
