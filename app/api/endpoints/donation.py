from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.core.db import get_async_session
from app.core.services import investing_sevice
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User

router = APIRouter()


@router.get(
    "/",
    response_model=List[schemas.DonationAdminDBResponseResponse],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Получает список всех пожертвований.
    """
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.post(
    "/",
    response_model=schemas.DonationDBResponse,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: schemas.DonationCreateRequest,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Сделать пожертвование."""
    new_donation = await donation_crud.create(donation, session, user)
    await investing_sevice.investment(new_donation, CharityProject, session)
    return new_donation


@router.get(
    "/my",
    response_model=List[schemas.DonationDBResponse],
    response_model_exclude_none=True,
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Получить список моих пожертвований."""
    donations = await donation_crud.get_by_user(user, session)
    return donations
