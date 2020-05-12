# start from an official image
FROM python:3.6
LABEL net.juniper.vendor "Juniper Networks"
LABEL description "UFTS"
ARG UFTS_UID
ARG UFTS_GID

# arbitrary location choice: you can change the directory
RUN mkdir -p /opt/services/ufts/src
WORKDIR /opt/services/ufts/src
RUN groupadd -f -g "${UFTS_GID}" -r celery && useradd -u "${UFTS_UID}" --no-log-init -r -g "${UFTS_GID}" celery
RUN mkdir -p /var/run/celery/
RUN chown celery:celery /var/run/celery
# install our dependencies
# we use --system flag because we don't need an extra virtualenv
COPY Pipfile Pipfile.lock /opt/services/ufts/src/
RUN pip install pipenv && pipenv install --system
USER celery:celery
