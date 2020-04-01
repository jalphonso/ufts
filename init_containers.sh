#!/usr/bin/env bash

docker run -d -p 8500:8500 --name=consul --restart unless-stopped \
    consul agent -server -bootstrap-expect 1 -node=myconsulnode  -client=0.0.0.0 -ui

docker run -d --restart unless-stopped --name=registrator --net=host\
  -v /var/run/docker.sock:/tmp/docker.sock gliderlabs/registrator:latest \
  -internal=true \
  consul://`docker inspect consul --format {{.NetworkSettings.Networks.bridge.IPAddress}}`:8500
