from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity import CharityProject


class CRUDCharity(CRUDBase):

    async def get(
            self,
            charity_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(self.model.id == charity_id)
        )
        return db_obj.scalars().first()

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict()

        for field in obj_data:
            setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_charity_id_by_name(
            self,
            charity_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_charity_id = await session.execute(
            select(charity_name.id).where(
                CharityProject.name == charity_name
            )
        )
        db_charity_id = db_charity_id.scalars().first()
        return db_charity_id


charity_crud = CRUDCharity(CharityProject)