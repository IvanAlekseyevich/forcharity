from fastapi import FastAPI

from app.api.routers import main_router
from app.core.settings import settings

start_app = FastAPI(title=settings.app_title, description=settings.app_description)
start_app.include_router(main_router)
