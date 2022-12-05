from fastapi import FastAPI

from app.api.routers import charity_project_router, donation_router, user_router
from app.core.settings import settings

app = FastAPI(title=settings.app_title, description=settings.app_description)
app.include_router(charity_project_router)
app.include_router(donation_router)
app.include_router(user_router)
