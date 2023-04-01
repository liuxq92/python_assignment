import os 

from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_URL = f'mysql+pymysql://{os.getenv("MYSQL_USER")}:{os.getenv("MYSQL_PASSWD")}@{os.getenv("MYSQL_HOST")}:{os.getenv("MYSQL_PORT")}/python_assignment'

settings = Settings()