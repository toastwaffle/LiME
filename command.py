#!/usr/bin/env python3
"""Script access for LiME."""

import os
import sys
import typing

import flask_script
import flask_migrate

from lime import app
from lime.database import db
from lime.database import models # pylint: disable=unused-import
from lime.scripts import cron
from lime.scripts import run_bpython
from lime.system import setup

# pylint: disable=unused-import,ungrouped-imports,invalid-name
if typing.TYPE_CHECKING:
  import flask
# pylint: enable=unused-import,ungrouped-imports,invalid-name


def get_app(config: str) -> 'flask.Flask':
  """Load the appropriate config into the app."""
  lime_dir = os.path.realpath(__file__).replace('command.py', 'lime')

  config_files = [
      filename[:-3]
      for filename in os.listdir(os.path.join(lime_dir, 'config'))
      if filename.startswith(config) and filename.endswith('.py')
  ]

  if not config_files:
    sys.exit('No matching config file.')

  if len(config_files) > 1:
    sys.exit('Ambiguous config argument. Candidates: {0}'.format(
        ', '.join(config_files)))

  if not setup.configure_app(config_files[0]):
    sys.exit('Could not load config file {0}.py'.format(
        os.path.join(lime_dir, 'config', config_files[0])))

  return app.APP


def main():
  """Set up and run the Flask-Script manager."""
  flask_script.Server.help = 'Run the development server'

  flask_migrate.Migrate(app.APP, db.DB)

  manager = flask_script.Manager(get_app, with_default_commands=False)

  manager.add_option('config', help="Configuration file to load (prefix match)")

  manager.add_command('bpython', run_bpython.BpythonCommand)
  manager.add_command('cron', cron.CronCommand)
  manager.add_command('db', flask_migrate.MigrateCommand)
  manager.add_command('run', flask_script.Server)

  try:
    manager.run()
  except SystemExit as exc:
    print(exc)


if __name__ == '__main__':
  main()
