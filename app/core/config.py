from pydantic import BaseModel


class Setting(BaseModel):
    app_title: str = 'Благотворительный проект QRKot'
    app_description: str = 'Фонд собирает пожертвования на различные целевые проекты'
    database_url: str
    hash_gen_key: str = 'Secret'

    class Config():
        env_file = '.env'


settings = Setting()
