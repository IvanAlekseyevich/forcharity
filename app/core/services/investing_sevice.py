from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import CharityProject, Donation
from app.core.services import close_service


def reinvestment(
    new_obj: Union[CharityProject, Donation],
    open_obj: Union[CharityProject, Donation],
):
    """Перераспределяет средства между проектами и пожертвованиями."""
    to_close_new_obj = new_obj.full_amount - new_obj.invested_amount
    to_close_open_obj = open_obj.full_amount - open_obj.invested_amount
    if to_close_new_obj <= to_close_open_obj:
        open_obj.invested_amount += to_close_new_obj
        new_obj.invested_amount += to_close_new_obj
    else:
        open_obj.invested_amount += to_close_open_obj
        to_close_new_obj -= to_close_open_obj
        new_obj.invested_amount += to_close_open_obj
    return new_obj, open_obj


async def investment(
    new_obj: Union[CharityProject, Donation],
    model: Union[CharityProject, Donation],
    session: AsyncSession,
) -> None:
    """
    Перебирает открытые проекты/пожертвования,
    закрывает пожертвования/проекты при достижении лимита.
    При создании пожертвования перебирает открытые проекты.
    При создании проекта перебирает свободные пожертвования.

    :param new_obj: - только что созданное пожертвование/проект
    :param model:  - модель, открытые объекты которой мы будем перебирать.
    """
    all_open_obj = await session.execute(
        select(model).where(model.fully_invested == False)
    )
    all_open_obj = all_open_obj.scalars().all()
    for open_obj in all_open_obj:
        new_obj, open_obj = reinvestment(new_obj, open_obj)
        if open_obj.invested_amount == open_obj.full_amount:
            open_obj = close_service.set_close(open_obj)
        session.add(open_obj)
        if new_obj.invested_amount == new_obj.full_amount:
            new_obj = close_service.set_close(new_obj)
            break
    session.add(new_obj)
    await session.commit()
    await session.refresh(new_obj)
