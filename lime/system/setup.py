# coding: utf-8
"""Functions for setting up components of the system."""

import inspect

import flask

from .. import app
from ..views import all_views


APP = app.APP


def load_config(environment=None):
  """Load the configuration files according to the environment."""
  return (
    APP.config.from_pyfile('config/default.py', silent=False) and
    environment is None or
    APP.config.from_pyfile('config/{0}.py'.format(environment), silent=False)
  )


def configure_jinja2():
  """Tell jinja2 to trim whitespace from blocks."""
  APP.jinja_env.trim_blocks = True
  APP.jinja_env.lstrip_blocks = True


def load_blueprints():
  """Attach the various blueprints to the app."""
  for _name, blueprint in inspect.getmembers(
      all_views,
      lambda m: isinstance(m, flask.Blueprint)
  ):
    app.APP.register_blueprint(blueprint)


def configure_app(environment=None):
  """Run all the configuration steps to set up the app."""
  if not load_config(environment):
    return False

  configure_jinja2()
  load_blueprints()

  return True
