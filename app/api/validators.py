from typing import Union

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import CharityProject
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreateRequest,
    CharityProjectUpdateRequest,
)


async def check_name_duplicate(
    project: Union[CharityProjectCreateRequest, CharityProjectUpdateRequest],
    session: AsyncSession,
) -> None:
    """Проверяет оригинальность названия проекта."""
    project_id = await charity_project_crud.get_by_name(project.name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail="Проект с таким именем уже существует!",
        )


def check_charity_project_close(
    project: CharityProject,
) -> None:
    """Проверяет, закрыт ли проект."""
    if project.fully_invested:
        raise HTTPException(
            status_code=400, detail="Закрытый проект нельзя редактировать!"
        )


def check_invested_before_edit(
    project: CharityProject,
    project_request: CharityProjectUpdateRequest,
) -> None:
    """Проверяет сумму, инвестированную в проект."""
    if (
        project_request.full_amount is not None
        and project.invested_amount > project_request.full_amount
    ):
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


async def update_charity_project(
    project: CharityProject,
    project_request: CharityProjectUpdateRequest,
    session: AsyncSession,
) -> None:
    check_charity_project_close(project)
    await check_name_duplicate(project_request, session)
    check_invested_before_edit(project, project_request)


def delete_charity_project(
    project: CharityProject,
) -> None:
    check_invested_before_delete(project)
    check_charity_project_close(project)
