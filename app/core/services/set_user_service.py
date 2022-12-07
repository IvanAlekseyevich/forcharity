from typing import Optional, Union

from app.core.models import CharityProject, Donation, User


def set_user(
    request_obj,
    obj_model: Union[CharityProject, Donation],
    user: Optional[User],
) -> Union[CharityProject, Donation]:
    """Устанавливает текущего пользователя для объекта, если он передан."""
    request_object = request_obj.dict()
    if user is not None:
        request_object["user_id"] = user.id
    new_obj = obj_model(**request_object)
    return new_obj
