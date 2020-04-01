#!/usr/bin/env bash

docker stop consul
docker stop registrator
docker stop consul-tpl
docker rm consul-tpl
docker-compose down