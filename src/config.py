from datetime import timedelta
from os import getenv

from dotenv import load_dotenv

load_dotenv()



SECRET_KEY = getenv("SECRET_KEY")

ALGORITHM = "HS256"
EXPIRATION_TIME = timedelta(minutes=30)


DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASS = getenv("DB_PASS")

TEST_DB_HOST = getenv('TEST_DB_HOST')
TEST_DB_PORT = getenv('TEST_DB_PORT')
TEST_DB_NAME = getenv('TEST_DB_NAME')
TEST_DB_USER = getenv('TEST_DB_USER')
TEST_DB_PASS = getenv('TEST_DB_PASS')


SMTP_USER = getenv("EMAIL_HOST_USER")
SMTP_PASSWORD = getenv("EMAIL_HOST_PASSWORD")
REDIS_HOST = getenv("REDIS_HOST")
REDIS_PORT = getenv("REDIS_PORT")
