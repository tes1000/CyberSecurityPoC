FROM python:latest

RUN apt update

RUN apt install sqlite3

WORKDIR /usr/app/src/

RUN mkdir templates

RUN pip install flask

RUN pip install jinja2

COPY ./app.py ./app.py
COPY ./index.html templates/index.html

CMD ["python", "app.py"]