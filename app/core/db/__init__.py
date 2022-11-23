<<<<<<< HEAD
from .charity_project import CharityProject
from .db import Base, get_async_session
from .donation import Donation
from .user import User
=======
from .db import get_async_session, Base  # Base импортирован для прохождения тестов
from .charity_project import charity_project_crud
from .donation import donation_crud
>>>>>>> origin/dev
