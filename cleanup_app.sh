#!/usr/bin/env bash

docker stop consul
docker stop registrator
docker stop consul-tpl
if [[ -f ".venv/bin/activate" ]]; then
    . .venv/bin/activate && docker-compose down --remove-orphans
else
    docker-compose down --remove-orphans
fi
docker rm consul
docker rm registrator
docker rm consul-tpl
if [[ -f ".venv/bin/activate" ]]; then
    . .venv/bin/activate && docker-compose down
else
    docker-compose down
fi