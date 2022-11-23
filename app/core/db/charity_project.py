<<<<<<< HEAD
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.db.db import Base


class CharityProject(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime)
    close_date = Column(DateTime)

    def __repr__(self):
        return f"Проект: {self.name}, требуемая сумма {self.full_amount}, инвестировано {self.invested_amount}, статус {self.fully_invested}"
=======
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

<<<<<<<< HEAD:app/crud/charity_project.py
from app.core.db import CharityProject
from app.crud.base import CRUDBase
========
from app.core.db.base import CRUDBase
from app.models.charity_project import CharityProject
>>>>>>>> origin/dev:app/core/db/charity_project.py


class CRUDCharityProject(CRUDBase):
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
            if field in update_data and update_data[field] is not None:
                setattr(db_obj, field, update_data[field])
        if db_obj.full_amount == db_obj.invested_amount:
            db_obj = self.set_close(db_obj)
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

    async def get_charity_project_id_by_name(
        self,
        charity_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_charity_id = await session.execute(
            select(self.model.id).where(self.model.name == charity_name)
        )
        db_charity_id = db_charity_id.scalars().first()
        return db_charity_id


charity_project_crud = CRUDCharityProject(CharityProject)
>>>>>>> origin/dev
