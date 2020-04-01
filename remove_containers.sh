#!/usr/bin/env bash

docker stop consul
docker stop registrator
docker stop consul-tpl
docker-compose down
docker rm consul
docker rm registrator
docker rm consul-tpl
docker-compose down
