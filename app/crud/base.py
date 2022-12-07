from datetime import datetime
from typing import List, Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import CharityProject, Donation
from app.core.models import User


class CRUDBase:
    def __init__(self, model):
        self._model = model

    async def get_all(
        self,
        session: AsyncSession,
    ) -> List[Union[CharityProject, Donation]]:
        """Возвращает все объекты из БД текущей модели."""
        db_objs = await session.execute(select(self._model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None,
    ) -> Union[CharityProject, Donation]:
        """Создает объект текущей модели."""
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data["user_id"] = user.id
        db_obj = self._model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
