from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_base


async def investment(
        new_obj,
        model,
        session: AsyncSession,
) -> None:
    all_open_obj = await session.execute(select(model).where(model.fully_invested == False))
    all_open_obj = all_open_obj.scalars().all()
    to_close_new_obj = new_obj.full_amount - new_obj.invested_amount
    for open_obj in all_open_obj:
        to_close_open_obj = open_obj.full_amount - open_obj.invested_amount
        if to_close_new_obj <= to_close_open_obj:
            open_obj.invested_amount += to_close_new_obj
            new_obj.invested_amount += to_close_new_obj
            new_obj = await crud_base.set_close(new_obj)
            if to_close_new_obj == to_close_open_obj:
                open_obj = await crud_base.set_close(open_obj)
            session.add(new_obj)
            session.add(open_obj)
            break
        else:
            open_obj.invested_amount += to_close_open_obj
            to_close_new_obj -= to_close_open_obj
            new_obj.invested_amount += to_close_open_obj
            open_obj = await crud_base.set_close(open_obj)
            session.add(new_obj)
            session.add(open_obj)
            continue
    await session.commit()
    await session.refresh(new_obj)
