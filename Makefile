.PHONY: venv develop prepare start stop restart monitor migrate testdata save load clean wipe freshinstall
docker-images-path=docker-images

venv:
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv && \
		. .venv/bin/activate && \
		pip3 install -q -U pip && \
		pip3 install -q -r requirements-docker.txt;\
	fi

develop: venv
	. .venv/bin/activate && \
	./docker-compose.py -g && \
	docker-compose pull && \
	docker pull consul && \
	docker pull gliderlabs/registrator:master && \
	docker-compose build
	docker build -t consul-template:custom -f Dockerfile-consul-template .

prepare: venv
	. .venv/bin/activate && \
	./docker-compose.py -g
	./init_app.sh
	mkdir -p logs media software reports
	sleep 30

start:
	./start_app.sh
	sleep 30

stop:
	./stop_app.sh

restart: stop start

monitor:
	-@./monitor_app.sh || true

migrate:
	docker exec app0 python manage.py migrate

testdata:
	docker exec app0 bash utilities/loaddefault_data.sh

status:
	docker ps -a
	docker images
	docker network ls
	docker volume ls

save:
	@if [ ! -d "docker-images" ]; then \
		mkdir -p docker-images;\
	fi
	@for image in $$(docker images --format "{{.Repository}}:{{.Tag}}"); do \
		filename="$(docker-images-path)/$${image//[\:|\/]/-}.tar"; \
		docker save -o $$filename $$image; \
	done

load:
	@for image in $$(ls docker-images); do \
		docker load -i $(docker-images-path)/$$image; \
	done

clean:
	find . -name '*.retry' -print | xargs rm -f || true
	find . -name '*.pyc' -print | xargs rm -f || true
	find . -name '__pycache__' -print | xargs rmdir || true
	./cleanup_app.sh

wipe: clean
	docker system prune -af
	docker volume prune -f
	rm -rf logs media software reports sent_emails

fresh_install: wipe develop prepare start migrate status

clean_start: clean prepare start

build_save_images: wipe develop save

offline_install: load prepare start migrate status
