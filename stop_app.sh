#!/usr/bin/env bash

docker stop consul-tpl
docker rm consul-tpl
. .venv/bin/activate && docker-compose down --remove-orphans