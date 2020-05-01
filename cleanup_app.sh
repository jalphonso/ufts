#!/usr/bin/env bash

docker stop consul
docker stop registrator
docker stop consul-tpl
if [[ -f ".venv/bin/activate" ]]; then
    . .venv/bin/activate && docker-compose down --remove-orphans
else
    docker-compose down --remove-orphans
fi
docker rm -f consul
docker rm -f registrator
docker rm -f consul-tpl
if [[ -f ".venv/bin/activate" ]]; then
    . .venv/bin/activate && docker-compose down
else
    docker-compose down
fi
docker rmi -f celery haproxy haproxy:custom ufts-app consul-template:custom
rm -f docker-compose.yml