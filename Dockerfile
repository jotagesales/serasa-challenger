FROM python:3.11-slim

RUN apt-get update -y &&\
    apt-get install -y bash build-essential python3-dev  default-libmysqlclient-dev pkg-config libcurl4-openssl-dev


ARG DEPLOY_PATH='/app'

RUN mkdir -p $DEPLOY_PATH

ADD accounts/ $DEPLOY_PATH/accounts
ADD billing/ $DEPLOY_PATH/billing
ADD hosting/ $DEPLOY_PATH/hosting
ADD marketing/ $DEPLOY_PATH/marketing
ADD sites/ $DEPLOY_PATH/sites
ADD static/ $DEPLOY_PATH/static
ADD templates/ $DEPLOY_PATH/templates

ADD requirements-dev.txt $DEPLOY_PATH/requirements-dev.txt
ADD requirements.txt $DEPLOY_PATH/requirements.txt
ADD package.json $DEPLOY_PATH/package.json
ADD tailwind.config.js $DEPLOY_PATH/tailwind.config.js
ADD manage.py $DEPLOY_PATH/manage.py


WORKDIR $DEPLOY_PATH

RUN pip install -U pip setuptools wheel
RUN pip install -r requirements-dev.txt

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "hosting.wsgi:application", "--access-logfile", "-", "--error-logfile", "-"]
