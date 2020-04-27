#!/usr/bin/env bash

docker stop consul-tpl
docker rm consul-tpl
if [[ -f ".venv/bin/activate" ]]; then
    . .venv/bin/activate && docker-compose down --remove-orphans
else
    docker-compose down --remove-orphans
fi