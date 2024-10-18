FROM python:3.11-slim

RUN apt-get update -y &&\
    apt-get install -y -- build-essential git libpq-dev

ARG DEPLOY_PATH='/app'

RUN mkdir -p $DEPLOY_PATH

ADD serasa/ $DEPLOY_PATH/serasa
ADD apps/ $DEPLOY_PATH/apps
ADD manage.py $DEPLOY_PATH/manage.py
ADD requirements.txt $DEPLOY_PATH/requirements.txt

WORKDIR $DEPLOY_PATH

RUN pip install -U pip setuptools wheel
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "serasa.wsgi.application"]
