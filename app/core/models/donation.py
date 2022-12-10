from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Text,
)

from app.core.models.base import Base


class Donation(Base):
    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    close_date = Column(DateTime)

    def __repr__(self):
        return (
            f"<User_id: {self.user_id}, "
            f"full_amount: {self.full_amount}, "
            f"invested_amount: {self.invested_amount}, "
            f"fully_invested: {self.fully_invested}>"
        )
