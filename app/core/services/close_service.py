from datetime import datetime
from typing import Union

from app.core.models import CharityProject, Donation


def set_close(obj: Union[CharityProject, Donation]) -> Union[CharityProject, Donation]:
    """Закрывает объект и добавляет дату закрытия."""
    if obj.full_amount == obj.invested_amount:
        obj.fully_invested = True
        obj.close_date = datetime.now()
    return obj
