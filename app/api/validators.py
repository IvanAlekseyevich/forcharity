from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity import charity_crud
from app.models import CharityProject


async def check_name_duplicate(
        charity_name: str,
        session: AsyncSession,
) -> None:
    charity_id = await charity_crud.get_charity_id_by_name(charity_name, session)
    if charity_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_exists(
        charity_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity = await charity_crud.get(charity_id, session)
    if charity is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity


async def check_charity_close(
        charity: CharityProject,
) -> None:
    if charity.fully_invested is False:
        raise HTTPException(
            status_code=422,
            detail='Проект закрыт!'
        )


async def check_charity_donations(
        charity: CharityProject,
) -> None:
    if charity.invested_amount != 0:
        raise HTTPException(
            status_code=422,
            detail='В проект уже внесены средства!'
        )
