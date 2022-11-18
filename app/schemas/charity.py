from pydantic import BaseModel, Field, PositiveInt, validator


class CharityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    full_amount: PositiveInt


class CharityProjectCreate(CharityBase):
    pass


class CharityProjectUpdate(CharityBase):
    @validator('name')
    def name_update(cls, value):
        if value is None:
            raise ValueError('Имя проекта не может быть пустым')
        return value


class CharityProjectDB(CharityBase):
    id: int
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime
    close_date: datetime

    class Config:
        orm_mode = True
