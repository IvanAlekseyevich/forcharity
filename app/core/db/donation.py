from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text

from app.core.db.base import Base


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
