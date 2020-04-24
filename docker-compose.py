#!/usr/bin/env python

from compose.cli.main import main as compose_main
from pathlib import Path
from ruamel.yaml import YAML

import argparse
import jinja2
import sys

yaml = YAML()

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--app', metavar='number of app instances',
                    default=1, type=int,
                    help='Specify an numnber of app instances to run')
parser.add_argument('-w', '--web', metavar='number of web instances',
                    default=1, type=int,
                    help='Specify an numnber of web instances to run')

(args, extras) = parser.parse_known_args()

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader, autoescape=True)
TEMPLATE_FILE = "docker-compose.j2"
template = templateEnv.get_template(TEMPLATE_FILE)
compose_file = template.render(num_web=args.web, num_app=args.app)
compose_yml = yaml.load(compose_file)
compose_file_path = Path("docker-compose.yml")
yaml.dump(compose_yml, compose_file_path)

sys.argv[:] = ['docker-compose'] + extras
compose_main()