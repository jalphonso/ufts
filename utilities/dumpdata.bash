#!/usr/bin/env bash

./manage.py dumpdata --indent 4 --format json --natural-primary --natural-foreign auth.group -o fixtures/auth_group.json
./manage.py dumpdata --indent 4 --format json --natural-primary --natural-foreign auth.group -o fixtures/documentation.json
./manage.py dumpdata --indent 4 --format json --natural-primary --natural-foreign auth.group -o fixtures/jsa.json
./manage.py dumpdata --indent 4 --format json --natural-primary --natural-foreign auth.group -o fixtures/uploads.json
./manage.py dumpdata --indent 4 --format json --natural-primary --natural-foreign auth.group -o fixtures/users.json