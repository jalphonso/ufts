.PHONY: develop tag_for_prod prepare start stop restart scale monitor migrate testdata status \
				save load clean wipe fresh_install clean_start build_save_images offline_install
export DOCKER_IMAGES_PATH=docker-images
export APP_VERSION=1.0
export SERVICE_NETWORK=172.20.0.0/24
export CONSUL_IP=172.20.0.2
export CONSUL_PORT=8500
export CONSUL_TPL_IP=172.20.0.3
export SLEEP_TIMER=30

PWD=$(shell pwd)
APP=1
WEB=1

develop:
	rm -f docker/app/Pipfile docker/app/Pipfile.lock docker/celery/Pipfile docker/celery/Pipfile.lock || true
	cp Pipfile Pipfile.lock docker/app/
	cp Pipfile Pipfile.lock docker/celery/
	./docker-compose.py --version dev; \
	docker-compose build
	docker build -t ufts-consul-template:dev docker/consul-tpl
	docker build -t ufts-consul:dev docker/consul
	docker build -t ufts-registrator:dev docker/registrator

tag_for_prod:
	docker image tag ufts-consul:dev ufts-consul:$(APP_VERSION)
	docker image tag ufts-consul-template:dev ufts-consul-template:$(APP_VERSION)
	docker image tag ufts-registrator:dev ufts-registrator:$(APP_VERSION)
	docker image tag ufts-celery:dev ufts-celery:$(APP_VERSION)
	docker image tag ufts-app:dev ufts-app:$(APP_VERSION)
	docker image tag ufts-nginx:dev ufts-nginx:$(APP_VERSION)
	docker image tag ufts-haproxy:dev ufts-haproxy:$(APP_VERSION)
	docker image tag ufts-redis:dev ufts-redis:$(APP_VERSION)
	docker image tag ufts-postgres:dev ufts-postgres:$(APP_VERSION)

prepare:
	./docker-compose.py --version $(APP_VERSION); \
	docker network create --subnet $(SERVICE_NETWORK) ufts_service_discovery_network || true
	docker run -d --name=consul --restart always --net=ufts_service_discovery_network --ip $(CONSUL_IP)\
		-e SERVICE_8300_NAME=consul-8300 -e SERVICE_8301_NAME=consul-8301 -e SERVICE_8302_NAME=consul-8302 -e SERVICE_8500_NAME=consul-8500 \
		-e SERVICE_8600_NAME=consul-8600 \
		ufts-consul:$(APP_VERSION) agent -server -bootstrap-expect 1 -node=myconsulnode  -client=0.0.0.0 -ui

	docker run -d --restart always --name=registrator --net=host \
		-v /var/run/docker.sock:/tmp/docker.sock ufts-registrator:$(APP_VERSION) \
		-internal \
		-useIpFromLabel=service_ip \
		consul://$(CONSUL_IP):$(CONSUL_PORT)

	mkdir -p logs media software reports
	sleep $(SLEEP_TIMER)

start:
	docker-compose up --remove-orphans -d || exit 1
	docker run -d --restart always --name consul-tpl -e CONSUL_TEMPLATE_LOG=debug  \
		--net=ufts_service_discovery_network --ip $(CONSUL_TPL_IP)  \
		-v /var/run/docker.sock:/var/run/docker.sock  \
		-v $(PWD)/config/consul/:/tmp/consul  \
		-v $(PWD)/config/web-haproxy/:/tmp/web-haproxy  \
		-v $(PWD)/config/app-haproxy/:/tmp/app-haproxy  \
		ufts-consul-template:$(APP_VERSION) \
		-template "/tmp/consul/web-haproxy.ctmpl:/tmp/web-haproxy/haproxy.cfg:docker  \
		kill -s HUP web-lb" \
		-template "/tmp/consul/app-haproxy.ctmpl:/tmp/app-haproxy/haproxy.cfg:docker  \
		kill -s HUP app-lb" \
		-consul-addr $(CONSUL_IP):$(CONSUL_PORT)
	sleep $(SLEEP_TIMER)

stop:
	docker stop consul-tpl || true
	docker rm -f consul-tpl || true
	docker-compose down --remove-orphans || true

restart: stop start

scale:
	./docker-compose.py --version $(APP_VERSION) -a$(APP) -w$(WEB)
	docker-compose up --remove-orphans -d || exit 1

monitor:
	docker-compose logs -f || true

migrate:
	docker exec app0 python manage.py migrate

testdata:
	docker exec app0 bash utilities/loaddefault_data.sh

status:
	docker ps -a
	docker images
	docker network ls
	docker volume ls

save: tag_for_prod
	@if [ ! -d $(DOCKER_IMAGES_PATH) ]; then \
		mkdir -p $(DOCKER_IMAGES_PATH);\
	fi

	@for image in $$(docker images -f reference="ufts*$(APP_VERSION)" --format "{{.Repository}}:{{.Tag}}"); do \
		filename="$(DOCKER_IMAGES_PATH)/$${image//[\:|\/]/-}.tar"; \
		docker save -o $$filename $$image; \
	done

load:
	@for image in $$(ls docker-images); do \
		docker load -i $(DOCKER_IMAGES_PATH)/$$image; \
	done

clean: stop
	find . -name '*.retry' -print | xargs rm -f || true
	find . -name '*.pyc' -print | xargs rm -f || true
	find . -name '__pycache__' -print | xargs rmdir || true
	docker stop consul || true
	docker stop registrator || true
	docker rm -f consul || true
	docker rm -f registrator || true
	docker-compose down || true
	rm -f docker-compose.yml || true

wipe: clean
	docker system prune -af
	docker volume prune -f
	rm -rf logs media software reports sent_emails

fresh_install: wipe develop prepare start migrate status

clean_start: clean prepare start

build_save_images: wipe develop save

offline_install: load prepare start migrate status
