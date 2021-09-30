FROM python:3.6
MAINTAINER Nikita-Boyarskikh <N02@yandex.ru>

ARG PROJECT_ROOT
ARG PROJECT_NAME
ARG PORT

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /tmp/$PROJECT_ROOT
COPY conf/python/requirements.pip /tmp/$PROJECT_ROOT/
RUN pip install -r /tmp/$PROJECT_ROOT/requirements.pip &&\
    rm -rf /tmp/$PROJECT_ROOT

RUN mkdir -p /$PROJECT_ROOT/$PROJECT_NAME
WORKDIR /$PROJECT_ROOT/$PROJECT_NAME

COPY ./$PROJECT_NAME /$PROJECT_ROOT/$PROJECT_NAME
COPY ./conf /$PROJECT_ROOT/conf

EXPOSE $PORT

ENTRYPOINT python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:$PORT
