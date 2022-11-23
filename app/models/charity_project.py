from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.db import Base


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
