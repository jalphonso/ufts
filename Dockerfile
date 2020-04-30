# start from an official image
FROM python:3.6
ARG UFTS_UID
ARG UFTS_GID
# arbitrary location choice: you can change the directory
RUN mkdir -p /opt/services/ufts/src
WORKDIR /opt/services/ufts/src
RUN groupadd -g "${UFTS_GID}" -r ufts && useradd -u "${UFTS_UID}" --no-log-init -r -g ufts ufts
# install our dependencies
# we use --system flag because we don't need an extra virtualenv
COPY Pipfile Pipfile.lock /opt/services/ufts/src/
RUN pip install pipenv && pipenv install --system

# expose the port 8000
EXPOSE 8000

RUN sed -i 's/load staticfiles/load static/g' /usr/local/lib/python3.6/site-packages/django_classification_banner/templates/django_classification_banner/classification.html
# define the default command to run when starting the container
USER ufts:ufts
CMD ["gunicorn", "-w", "3", "--chdir", "ufts", "--bind", ":8000", "ufts.wsgi:application"]
