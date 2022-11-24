from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db.base import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    pass
