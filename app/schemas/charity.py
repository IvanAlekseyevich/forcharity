from pydantic import BaseModel, Field, PositiveInt


class CharityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    full_amount: PositiveInt


class CharityProjectCreate(CharityBase):
    pass


class CharityProjectUpdate(CharityBase):
    pass


class CharityProjectDB(CharityBase):
    id: int
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime
    close_date: datetime = None

    class Config:
        orm_mode = True
