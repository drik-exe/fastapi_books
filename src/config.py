from os import getenv
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()



SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRATION_TIME = timedelta(minutes=30)


DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASS = getenv("DB_PASS")


SMTP_USER = getenv("EMAIL_HOST_USER")
SMTP_PASSWORD = getenv("EMAIL_HOST_PASSWORD")
REDIS_HOST = getenv("REDIS_HOST")
REDIS_PORT = getenv("REDIS_PORT")
