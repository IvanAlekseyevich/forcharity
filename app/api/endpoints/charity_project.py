from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.api import validators
from app.core.db import charity_project_crud, get_async_session
from app.core.services import investing_sevice
from app.core.user import current_superuser
from app.models import Donation

router = APIRouter()


@router.get(
    "/",
    response_model=List[schemas.CharityProjectDBResponse],
    response_model_exclude={"close_date"},
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Получает список всех проектов"""
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    "/",
    response_model=schemas.CharityProjectDBResponse,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_charity_project(
    new_project: schemas.CharityProjectCreateRequest,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Создает благотворительный проект.
    """
    await validators.check_name_duplicate(new_project.name, session)
    new_project = await charity_project_crud.create(new_project, session)
    await investing_sevice.investment(new_project, Donation, session)
    return new_project


@router.patch(
    "/{project_id}",
    response_model=schemas.CharityProjectDBResponse,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    project_obj: schemas.CharityProjectUpdateRequest,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Закрытый проект нельзя редактировать, также нельзя установить требуемую сумму меньше уже вложенной.
    """
    project = await validators.get_charity_project_exists(project_id, session)
    validators.check_charity_project_close(project)
    await validators.check_name_duplicate(project_obj.name, session)
    if project_obj.full_amount is not None:
        validators.check_invested_before_edit(project, project_obj.full_amount)
    project = await charity_project_crud.update(project, project_obj, session)
    return project


@router.delete(
    "/{project_id}",
    response_model=schemas.CharityProjectDBResponse,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Удаляет проект. Нельзя удалить проект, в который уже были инвестированы средства, его можно только закрыть.
    """
    project = await validators.get_charity_project_exists(project_id, session)
    validators.check_invested_before_delete(project)
    validators.check_charity_project_close(project)
    project = await charity_project_crud.remove(project, session)
    return project
