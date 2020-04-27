.PHONY: venv install start stop restart clean

venv:
				@if [ ! -d ".venv" ]; then \
								python3 -m venv .venv && \
								. .venv/bin/activate && \
								pip3 install -q -U pip && \
								pip3 install -q -r requirements-docker.txt;\
				fi

install: venv
				. .venv/bin/activate && \
				./docker-compose.py build
				./init_app.sh
				docker build -t consul-template:custom -f Dockerfile-consul-template .

start:
				./start_app.sh

stop:
				./stop_app.sh

restart:
				./restart_app.sh

clean:
				find . -name '*.retry' -print | xargs rm
				find . -name '*.pyc' -print | xargs rm
				find . -name '__pycache__' -print | xargs rmdir
				./cleanup_app.sh

wipe: clean
				docker system prune -af
				docker volume prune -f