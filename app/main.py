from fastapi import FastAPI

from app.api.endpoints import charity_project_router, donation_router, user_router
from app.core.settings import settings

start_app = FastAPI(title=settings.app_title, description=settings.app_description)
start_app.include_router(charity_project_router)
start_app.include_router(donation_router)
start_app.include_router(user_router)
