from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud, donation_crud
from app.models import CharityProject, Donation


async def invest_project(
        new_project: CharityProject,
        session: AsyncSession,
):
    open_donations = await donation_crud.get_all_open(session)
    for donation in open_donations:
        free_donat = donation.full_amount - donation.invested_amount  # Свободный донат без заинвестированных
        need_project = new_project.full_amount - new_project.invested_amount  # Надо проекту денег
        if free_donat <= need_project:  # Если задоначено меньше либо ровно на проект
            new_project.invested_amount += free_donat  # Устанавливаем сумму из доната
            donation.invested_amount += free_donat  # Устанавливаем в донате что все деньги задоначены
            need_project -= free_donat
            free_donat = 0  # Устанавливаем свободный донат на нуле
        else:
            new_project.invested_amount += need_project
            free_donat -= need_project
            donation.invested_amount += need_project
            need_project = 0
        if need_project == 0:
            new_project.close_date = datetime.now()
            new_project.fully_invested = True
        if free_donat == 0:
            donation.close_date = datetime.now()
            donation.fully_invested = True
            break
        session.add(donation)
        session.add(new_project)
    await session.commit()
    await session.refresh(new_project)


async def invest_donation(
        new_donation: Donation,
        session: AsyncSession,
):
    open_projects = await charity_project_crud.get_all_open(session)
    for project in open_projects:  # Открытый проект
        free_donat = new_donation.full_amount - new_donation.invested_amount  # Свободный донат без заинвестированных уже
        need_project = project.full_amount - project.invested_amount  # Надо проекту денег
        if free_donat <= need_project:  # Если задоначено меньше либо ровно на проект
            project.invested_amount += free_donat  # Устанавливаем сумму из доната
            new_donation.invested_amount += free_donat  # Устанавливаем в донате что все деньги задоначены
            need_project -= free_donat
            free_donat = 0  # Устанавливаем свободный донат на нуле
        else:
            project.invested_amount += need_project
            free_donat -= need_project
            new_donation.invested_amount += need_project
            need_project = 0
        if need_project == 0:
            project.close_date = datetime.now()
            project.fully_invested = True
        if free_donat == 0:
            new_donation.close_date = datetime.now()
            new_donation.fully_invested = True
            break
        print(new_donation)
        print(project)
        session.add(new_donation)
        session.add(project)
    await session.commit()
    await session.refresh(new_donation)
