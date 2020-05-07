#!/usr/bin/env bash

docker network create --subnet 172.20.0.0/24 ufts_service_discovery_network || true
docker run -d -p 8500:8500 --name=consul --restart always --net=ufts_service_discovery_network --ip 172.20.0.2\
    consul agent -server -bootstrap-expect 1 -node=myconsulnode  -client=0.0.0.0 -ui

docker run -d --restart always --name=registrator --net=host \
    -v /var/run/docker.sock:/tmp/docker.sock gliderlabs/registrator:master \
    -internal \
    -useIpFromLabel=service_ip \
    consul://`docker inspect consul --format {{.NetworkSettings.Networks.ufts_service_discovery_network.IPAddress}}`:8500
