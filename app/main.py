from fastapi import FastAPI

from app.api.routers import main_router
from app.core.settings import settings

app = FastAPI(title=settings.app_title, description=settings.app_description)
app.include_router(main_router)
