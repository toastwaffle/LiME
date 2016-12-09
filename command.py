#!/usr/bin/env python3
# coding: utf-8
"""Script access for LiME."""

import os
import sys

import flask_script
import flask_migrate

from lime import app
from lime.database import db
from lime.database import models # pylint: disable=unused-import
from lime.scripts import cron
from lime.scripts import run_bpython
from lime.system import setup

LIME_DIR = os.path.realpath(__file__).replace('command.py', 'lime')

def get_app(config):
  """Load the appropriate config into the app."""
  config_files = [
    filename[:-3]
    for filename in os.listdir(os.path.join(LIME_DIR, 'config'))
    if filename.startswith(config)
    and filename.endswith('.py')
  ]

  if not config_files:
    print('No matching config file.')
  elif len(config_files) > 1:
    print(
      'Ambiguous config argument. Candidates: {0}'.format(
        ', '.join(config_files)
      )
    )
  elif not setup.configure_app(config_files[0]):
    print(
      'Could not load config file {0}.py'.format(
        os.path.join(LIME_DIR, 'config', config_files[0])
      )
    )
  else:
    return app.APP

  sys.exit(-1)

flask_script.Server.help = 'Run the development server'

MIGRATE = flask_migrate.Migrate(app.APP, db.DB)

MANAGER = flask_script.Manager(get_app, with_default_commands=False)

MANAGER.add_option('config', default=None,
                   help="Configuration file to load before running commands")

MANAGER.add_command('bpython', run_bpython.BpythonCommand)
MANAGER.add_command('cron', cron.CronCommand)
MANAGER.add_command('db', flask_migrate.MigrateCommand)
MANAGER.add_command('run', flask_script.Server)

if __name__ == '__main__':
  MANAGER.run()
