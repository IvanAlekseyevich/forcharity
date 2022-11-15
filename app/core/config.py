from pydantic import BaseModel


class Setting(BaseModel):
    app_title: str = 'Благотворительный фонд QRKot'
    app_description: str = 'Сервис для поддержки нуждающихся'
    database_url: str
    hash_gen_key: str = 'Secret'

    class Config():
        env_file = '.env'


settings = Setting()
