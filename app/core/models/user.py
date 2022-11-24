from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.models.base import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    pass
