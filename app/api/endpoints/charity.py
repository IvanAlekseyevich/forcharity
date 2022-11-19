from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate, check_charity_exists, check_charity_close, check_charity_donations
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity import charity_crud
from app.schemas.charity import CharityProjectDB, CharityProjectCreate, CharityProjectUpdate

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],  # Схема возврата всех проектов
)
async def get_all_charity(
        session: AsyncSession = Depends(get_async_session),
):
    """Получает список всех проектов"""
    all_charity = await charity_crud.get_multi(session)  # Запрос всех проектов
    return all_charity


@router.post(
    '/',
    response_model=CharityProjectDB,  # Схема ответа
    dependencies=[Depends(current_superuser)],  # Разрешить создание только суперюзером
)
async def create_new_charity(
        charity=CharityProjectCreate,  # Схема создания проекта
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    Создает благотворительный проект.
    """
    await check_name_duplicate(charity.name, session)  # Проверка дубликата названия
    new_charity = await charity_crud.create(charity, session)  # Создание проекта
    return new_charity


@router.patch(
    '/charity_id',
    response_model=CharityProjectDB,  # Схема возврата данных
    dependencies=[Depends(current_superuser)],  # Только для суперюзеров
)
async def partially_update_charity(
        charity_id=int,  # id проекта
        charity_obj=CharityProjectUpdate,  # Схема обновления проекта
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    Закрытый проект нельзя редактировать, также нельзя установить требуемую сумму меньше уже вложенной.
    """
    charity = await check_charity_exists(charity_id, session)  # Проверка существования проекта
    if charity_obj.name is not None:
        await check_charity_close(charity)  # Проверка закрыт ли проект
        await check_charity_donations(charity)  # Проверка задоначенной суммы в проект
        await check_name_duplicate(charity_obj.name, session)  # Проверка на дубликат имени
    charity = await charity_crud.update(charity, charity_obj, session)
    return charity


@router.delete(
    '/charity_id',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity(
        charity_id=int,  # id удаляемого проекта
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    Удаляет проект. Нельзя удалить проект, в который уже были инвестированы средства, его можно только закрыть.
    """
    charity = await check_charity_exist(charity_id, session)  # Проверка существования проекта
    await check_charity_donations(charity)  # Проверка доната проекта
    charity = await charity_crud.remove(charity, session)
    return charity
