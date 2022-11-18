from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.charity import CharityProjectDB, CharityProjectCreate, CharityProjectUpdate

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],  # Схема возврата всех проектов
)
async def get_all_charity(
        session: AsyncSession = Depends(get_async_session),
):
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
    """Только для суперюзеров."""
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
        charity_obj=CharityProjectUpdate,  # Схема обновления проекта с проверкой на пустое имя
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity = await check_charity_exists(charity_id, session)  # Проверка существования проекта
    if charity_obj.name is not None:
        await check_name_duplicate(charity_obj.name, session)  # Проверка на дубликат имени
        await check_donations(charity, charity_obj.full_amount, session)  # Проверка задоначенной суммы в проект
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
    """Только для суперюзеров."""
    charity = await check_charity_exist(charity_id, session)  # Проверка существования проекта
    await check_donations(charity, session)  # Проверка доната проекта
    charity = await charity_crud.remove(charity, session)
    return charity
