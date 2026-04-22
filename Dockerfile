#########################################################################
# Mount a config.json file into the container if running outside of K8s #
#########################################################################
FROM python:3.12-alpine

ARG     SERVICE_USER="paso"
ARG     SERVICE_GROUP="$SERVICE_USER"
# These must be set to match the permissions provided within k8s
ARG     UID=1000
ARG     GID=1000

USER    root
WORKDIR /app

RUN apk update && apk upgrade

RUN pip install pipenv flask gunicorn mysql-connector datetime

COPY api.py log.sh ./
COPY html html

EXPOSE 80

RUN adduser --disabled-password -u $UID -g $GID $SERVICE_USER $SERVICE_GROUP && chown -R $SERVICE_USER /app
USER $SERVICE_USER

ENV PYTHONPATH="/app"

ENTRYPOINT ["gunicorn", "-w", "4", "-b", ":80", "api:app"]
