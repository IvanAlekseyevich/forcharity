# QRKot

***QRKot - приложение для Благотворительного фонда***

## Возможности проекта QRKot

- Создание администратором благотворительных проектов
- Внесение пожертвований пользователями
- Автоматическое инвестирование в проекты из пожертвований
- Регистрация пользователей на основе FastAPI Users

## Технологии

- Python 3.9
- FastAPI 0.78
- SQLAlchemy 1.4.36
- Alembic 1.7.7

## Установка и запуск проекта

- В корневой папке создайте файл *.env* и добавьте в него свои данные (при необходимости):

```
APP_TITLE=         # Название приложения
APP_DESCRIPTION=   # Описание приложения
DATABASE_URL=      # Путь подключения к БД
HASH_GEN_KEY=      # Ключ для генерации хэша
```

- Установите зависимости

- Создайте миграции

```shell
alembic revision --autogenerate -m "First migration" 
```

- Установите миграции

```shell
alembic upgrade head
```

- Запустите проект

```shell
uvicorn app.main:app --reload
```

## Документации проекта QRKot

При запущенном проекте откройте одну из ссылкок в браузере:

```sh
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
```

## Мои профили

- [GitHub](https://github.com/pozarnik/)
- [LinkedIn](https://www.linkedin.com/in/ivan-alekseyevich/)

## License

MIT