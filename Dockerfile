FROM python:3.11

RUN mkdir /fastapi_books

WORKDIR /fastapi_books

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH /fastapi_books/src

#WORKDIR src

RUN chmod a+x docker/*.sh
#
#RUN alembic upgrade head

#CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

