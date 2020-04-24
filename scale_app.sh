#!/usr/bin/env bash

if [ "$1" != "" ]; then
    a="$1"
else
    a=1
fi
if [ "$2" != "" ]; then
    w="$2"
else
    w=1
fi

. .venv/bin/activate && ./docker-compose.py -a"$a" -w"$w" up --remove-orphans -d || exit 1