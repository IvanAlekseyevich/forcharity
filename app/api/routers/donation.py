from typing import List

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import CharityProject, get_async_session, User
from app.core.services import investing_sevice
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationDBResponse,
    DonationAdminDBResponse,
    DonationCreateRequest,
)

router = APIRouter(prefix="/donation", tags=["donations"])


@cbv(router)
class DonationCBV:
    session: AsyncSession = Depends(get_async_session)

    @router.get(
        "/",
        response_model=List[DonationAdminDBResponse],
        dependencies=[Depends(current_superuser)],
        response_model_exclude_none=True,
        summary="Получить список всех пожертвований.",
    )
    async def get_all_donations(self) -> DonationAdminDBResponse:
        """
        Только для суперюзеров.\n
        Получает список всех пожертвований.
        """
        all_donations = await donation_crud.get_all(self.session)
        return all_donations

    @router.post(
        "/",
        response_model=DonationDBResponse,
        response_model_exclude_none=True,
        summary="Сделать пожертвование.",
    )
    async def create_donation(
        self,
        donation: DonationCreateRequest,
        user: User = Depends(current_user),
    ) -> DonationDBResponse:
        """Создает пожертвование."""
        new_donation = await donation_crud.create(donation, self.session, user)
        await investing_sevice.investment(new_donation, CharityProject, self.session)
        return new_donation

    @router.get(
        "/my",
        response_model=List[DonationDBResponse],
        response_model_exclude_none=True,
        summary="Получить список моих пожертвований.",
    )
    async def get_user_donations(
        self,
        user: User = Depends(current_user),
    ) -> DonationDBResponse:
        """Возвращает список пожертвований текущего пользователя."""
        donations = await donation_crud.get_by_user(user, self.session)
        return donations
