#!/usr/bin/env python

from pathlib import Path
from ruamel.yaml import YAML

import argparse
import jinja2
import os
import sys

yaml = YAML()
TEMPLATE_FILE = "docker-compose.j2"

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--app', metavar='number of app instances',
                    default=1, type=int,
                    help='Specify a number of app instances to run')
parser.add_argument('-w', '--web', metavar='number of web instances',
                    default=1, type=int,
                    help='Specify a number of web instances to run')
parser.add_argument('-v', '--version',
                    required=True,
                    help='specify app version')

(args, extras) = parser.parse_known_args()

uid = os.getuid()
gid = os.getgid()
templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader, autoescape=True)

data = {
  'num_web':args.web,
  'num_app':args.app,
  'UID':uid,
  'GID':gid,
  'app_version':args.version
}

template = templateEnv.get_template(TEMPLATE_FILE)
compose_file = template.render(data)
compose_yml = yaml.load(compose_file)
compose_file_path = Path("docker-compose.yml")
yaml.dump(compose_yml, compose_file_path)
