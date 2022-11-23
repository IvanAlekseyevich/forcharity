from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    pass
