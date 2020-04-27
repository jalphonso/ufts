#!/usr/bin/env bash

if [[ -f ".venv/bin/activate" ]]; then
    . .venv/bin/activate && ./docker-compose.py -a1 -w1 up --remove-orphans -d || exit 1
else
    ./docker-compose.py -a1 -w1 up --remove-orphans -d || exit 1
fi

docker run -d --restart unless-stopped --name consul-tpl -e CONSUL_TEMPLATE_LOG=debug  \
-v /var/run/docker.sock:/var/run/docker.sock  \
-v /usr/local/bin/docker:/usr/bin/docker  \
-v $(pwd)/config/consul/:/tmp/consul  \
-v $(pwd)/config/web-haproxy/:/tmp/web-haproxy  \
-v $(pwd)/config/app-haproxy/:/tmp/app-haproxy  \
hashicorp/consul-template \
-template "/tmp/consul/web-haproxy.ctmpl:/tmp/web-haproxy/haproxy.cfg:docker  \
kill -s HUP '$(docker ps -aq --filter name=web-lb)'" \
-template "/tmp/consul/app-haproxy.ctmpl:/tmp/app-haproxy/haproxy.cfg:docker  \
kill -s HUP '$(docker ps -aq --filter name=app-lb)'" \
-consul-addr `docker inspect consul --format {{.NetworkSettings.Networks.bridge.IPAddress}}`:8500