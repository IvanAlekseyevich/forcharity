<<<<<<< HEAD
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text

from app.core.db.db import Base


class Donation(Base):
    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime)
    close_date = Column(DateTime)

    def __repr__(self):
        return f"Пользователь: {self.user_id}, пожертвовал {self.full_amount}, инвестировано {self.invested_amount}, статус {self.fully_invested}"
=======
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

<<<<<<<< HEAD:app/crud/donation.py
from app.core.db import Donation, User
from app.crud.base import CRUDBase
========
from app.core.db.base import CRUDBase
from app.models import Donation, User
>>>>>>>> origin/dev:app/core/db/donation.py


class CRUDDonation(CRUDBase):
    async def get_by_user(
        self,
        user: User,
        session: AsyncSession,
    ):
        donations = await session.execute(
            select(self.model).where(self.model.user_id == user.id)
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
>>>>>>> origin/dev
