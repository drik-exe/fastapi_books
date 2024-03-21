import smtplib
from email.message import EmailMessage

from celery import Celery

from src.config import SMTP_PASSWORD, SMTP_USER, REDIS_HOST, REDIS_PORT

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')


def get_email_template(username: str):
    email = EmailMessage()
    email['Subject'] = 'Number of  users using the app'
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER

    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Hello, {username}, this is your email</h1>',
        subtype='html'
    )
    return email


@celery.task
def send_email_report(username: str):
    email = get_email_template(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
