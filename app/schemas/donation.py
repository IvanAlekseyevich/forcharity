from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    create_date: datetime


class DonationAdminDB(DonationBase):
    create_date: datetime
    user_id: int
    invested_amount: int = 0
    fully_invested: bool = False
    close_date: datetime

    class Meta:
        orm_mode = True
