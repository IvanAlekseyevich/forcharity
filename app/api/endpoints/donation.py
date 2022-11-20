from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.schemas.donation import DonationAdminDB, DonationDB, DonationCreate
from app.services.investing import invest_donation

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationAdminDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    Получает список всех пожертвований.
    """
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Сделать пожертвование."""
    new_donation = await donation_crud.create(donation, session, user)
    new_donation = await invest_donation(new_donation, session)
    return new_donation


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Получить список моих пожертвований."""
    donations = await donation_crud.get_by_user(user, session)
    return donations
