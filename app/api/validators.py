from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import CharityProject
from app.crud.charity_project import charity_project_crud


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """Проверяет оригинальность названия проекта."""
    project_id = await charity_project_crud.get_charity_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail="Проект с таким именем уже существует!",
        )


async def get_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Возвращает объект проекта по его id."""
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(status_code=404, detail="Проект не найден!")
    return project


def check_charity_project_close(
    project: CharityProject,
) -> None:
    """Проверяет, закрыт ли проект."""
    if project.fully_invested is True:
        raise HTTPException(
            status_code=400, detail="Закрытый проект нельзя редактировать!"
        )


def check_invested_before_edit(project: CharityProject, new_amount: int) -> None:
    """Проверяет сумму, инвестированную в проект."""
    if project.invested_amount > new_amount:
        raise HTTPException(
            status_code=400, detail="Нельзя установить сумму, ниже уже вложенной!"
        )


def check_invested_before_delete(
    project: CharityProject,
) -> None:
    """Проверяет сумму, инвестированную в проект."""
    if project.invested_amount != 0:
        raise HTTPException(
            status_code=400,
            detail="В проект были внесены средства, не подлежит удалению!",
        )
