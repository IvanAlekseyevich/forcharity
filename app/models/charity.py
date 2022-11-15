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

    """
    name — уникальное название проекта, обязательное строковое поле; допустимая длина строки — от 1 до 100 символов включительно;
    description — описание, обязательное поле, текст; не менее одного символа;
    full_amount — требуемая сумма, целочисленное поле; больше 0;
    invested_amount — внесённая сумма, целочисленное поле; значение по умолчанию — 0;
    fully_invested — булево значение, указывающее на то, собрана ли нужная сумма для проекта (закрыт ли проект); значение по умолчанию — False;
    create_date — дата создания проекта, тип DateTime, должно добавляться автоматически в момент создания проекта.
    close_date — дата закрытия проекта, DateTime, проставляется автоматически в момент набора нужной суммы.
    """
