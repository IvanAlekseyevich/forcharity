from typing import List, Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import CharityProject, Donation, User
from app.core.services import set_user_service


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
        request_obj,
        session: AsyncSession,
        user: Optional[User] = None,
    ) -> Union[CharityProject, Donation]:
        """Создает объект текущей модели."""
        db_obj = set_user_service.set_user(request_obj, self._model, user)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
