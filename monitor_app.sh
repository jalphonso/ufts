#!/usr/bin/env bash

if [[ -f ".venv/bin/activate" ]]; then
    . .venv/bin/activate && docker-compose logs -f
else
    docker-compose logs -f
fi
