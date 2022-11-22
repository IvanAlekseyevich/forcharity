from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_charity_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return project


async def check_charity_project_close(
        project: CharityProject,
) -> None:
    if project.fully_invested is True:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_charity_project_donations(
        project: CharityProject,
        new_amount: int = None
) -> None:
    if new_amount is not None and project.invested_amount > new_amount:
        raise HTTPException(
            status_code=400,
            detail='Нельзя установить сумму, ниже уже вложенной!'
        )
    if new_amount is None and project.invested_amount != 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
