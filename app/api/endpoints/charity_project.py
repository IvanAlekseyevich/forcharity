from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate, check_charity_project_close,
    check_charity_project_donations, check_charity_project_exists
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
from app.services.investing import investment

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude={'close_date'},
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """Получает список всех проектов"""
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_charity_project(
        new_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Создает благотворительный проект.
    """
    await check_name_duplicate(new_project.name, session)
    new_project = await charity_project_crud.create(new_project, session)
    await investment(new_project, Donation, session)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
        project_id: int,
        project_obj: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Закрытый проект нельзя редактировать, также нельзя установить требуемую сумму меньше уже вложенной.
    """
    project = await check_charity_project_exists(project_id, session)
    await check_charity_project_close(project)
    await check_name_duplicate(project_obj.name, session)
    if project_obj.full_amount is not None:
        await check_charity_project_donations(project, project_obj.full_amount)
    project = await charity_project_crud.update(project, project_obj, session)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
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
    project = await check_charity_project_exists(project_id, session)
    await check_charity_project_donations(project)
    await check_charity_project_close(project)
    project = await charity_project_crud.remove(project, session)
    return project
