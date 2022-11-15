from datetime import datetime

from pydantic import BaseModel, Field, PositiveInt


class CharityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    full_amount: PositiveInt


class CharityCreate(CharityBase):
    pass


class CharityUpdate(CharityBase):
    pass


class CharityDB(CharityBase):
    id: int
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime = datetime.now()
    close_date: datetime

    class Config:
        orm_mode = True
