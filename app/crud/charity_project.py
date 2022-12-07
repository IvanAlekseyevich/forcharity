from typing import Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import CharityProject
from app.core.services import close_service
from app.crud.base import CRUDBase


class CRUDCharityProject(CRUDBase):
    async def get_or_none(
        self,
        charity_id: int,
        session: AsyncSession,
    ) -> Optional[CharityProject]:
        """Возвращает объект CharityProject из БД по его id, либо возвращает None."""
        db_obj = await session.execute(
            select(self._model).where(self._model.id == charity_id)
        )
        return db_obj.scalars().first()

    async def get_by_id(self, project_id: int, session: AsyncSession) -> CharityProject:
        """Возвращает объект CharityProject по его id, либо выбрасывает ошибку"""
        project = await self.get_or_none(project_id, session)
        if project is None:
            raise HTTPException(status_code=404, detail="Проект не найден!")
        return project

    async def update(
        self,
        db_obj: CharityProject,
        obj_in,
        session: AsyncSession,
    ) -> CharityProject:
        """Обновляет объект CharityProject и возвращает обновленный объект."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict()
        for field in obj_data:
            if field in update_data and update_data[field] is not None:
                setattr(db_obj, field, update_data[field])
        db_obj = close_service.set_close(db_obj)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj: CharityProject,
        session: AsyncSession,
    ) -> CharityProject:
        """Удаляет объект CharityProject по его id."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def exist_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> bool:
        """Проверяет существование полученного имени в БД, возвращает True/False."""
        db_project_id = await session.execute(
            select(select(self._model).where(self._model.name == project_name).exists())
        )
        return db_project_id.scalar()


charity_project_crud = CRUDCharityProject(CharityProject)
