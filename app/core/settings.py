from pydantic import BaseModel


class Settings(BaseModel):
    app_title: str = "Благотворительный фонд QRKot"
    app_description: str = "Сервис для поддержки нуждающихся"
    database_url: str = "sqlite+aiosqlite:///fastapi.db"
    hash_gen_key: str = "Secret"

    class Config:
        env_file = ".env"


settings = Settings()
