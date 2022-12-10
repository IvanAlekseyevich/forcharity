from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.models.base import Base


class CharityProject(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    close_date = Column(DateTime)

    def __repr__(self):
        return (
            f"<Name: {self.name}, "
            f"full_amount: {self.full_amount}, "
            f"invested_amount: {self.invested_amount}, "
            f"fully_invested: {self.fully_invested}>"
        )
