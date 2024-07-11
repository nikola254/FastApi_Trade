Fast API

uvicorn main:app --reload --host 8100


pip instal sqlalchemy alembic psycopg2 fastapi  pydant

alembic init migrations

alembic revision --autogenerate -m "DataBase creation"


alembic.ini
sqlalchemy.url = postgresql://%(DB_USER)s:%(DB_PASS)s@%(DB_HOST)s:%(DB_PORT)s/%(DB_NAME)s

.env
DB_USER = postgres
DB_PASS = 858585
DB_HOST = localhost
DB_PORT = 5432
DB_NAME = fastapi

config.py
from dotenv import load_dotenv
import os


load_dotenv(encoding='utf-8')

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")


env.py
from config import DB_HOST, DB_USER, DB_NAME, DB_PASS, DB_PORT

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
# добавленный код
section = config.config_ini_section
config.set_section_option(section, "DB_HOST", DB_HOST)
config.set_section_option(section, "DB_USER", DB_USER)
config.set_section_option(section, "DB_NAME", DB_NAME)
config.set_section_option(section, "DB_PASS", DB_PASS)
config.set_section_option(section, "DB_PORT", DB_PORT)



сделаем миграцию 

alembic upgrade ce709805e0c9 и указываем конкретный хеш
