#!/usr/bin/env bash

./manage.py loaddata fixtures/auth_group.json
./manage.py loaddata fixtures/users.json
./manage.py loaddata fixtures/documentation.json
./manage.py loaddata fixtures/jsa.json
./manage.py loaddata fixtures/uploads.json