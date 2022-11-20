from app.models import CharityProject, Donation
from sqlalchemy.ext.asyncio import AsyncSession


async def invest_charity(
        new_charity: CharityProject,
        session: AsyncSession,
):
    ...


async def invest_donation(
        new_donation: Donation,
        session: AsyncSession,
):
    ...
