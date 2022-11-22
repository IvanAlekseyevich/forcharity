from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityBase):
    pass


class CharityProjectUpdate(CharityBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    @validator('name')
    def name_update(cls, value):
        if value is None:
            raise ValueError('Имя не может быть пустым!')
        return value

    @validator('description')
    def description_update(cls, value):
        if value is None:
            raise ValueError('Описание не может быть пустым!')
        return value

    @validator('full_amount')
    def full_amount_update(cls, value):
        if value is None:
            raise ValueError('Требуемая сумма не может быть пустой!')
        return value


class CharityProjectDB(CharityBase):
    id: int
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime
    close_date: datetime = None

    class Config:
        orm_mode = True
