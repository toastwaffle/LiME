"""Functions for setting up components of the system."""

import typing

from .. import app
from ..database import db
from ..util import api

# pylint: disable=unused-import,ungrouped-imports,invalid-name
if typing.TYPE_CHECKING:
  from typing import (
      Optional,
  )
# pylint: enable=unused-import,ungrouped-imports,invalid-name

APP = app.APP
DB = db.DB


def load_config(environment: 'Optional[str]' = None) -> bool:
  """Load the configuration files according to the environment."""
  return (
      APP.config.from_pyfile('config/default.py', silent=False) and
      environment is None or
      APP.config.from_pyfile('config/{0}.py'.format(environment), silent=False)
  )


def configure_jinja2() -> None:
  """Tell jinja2 to trim whitespace from blocks."""
  APP.jinja_env.trim_blocks = True
  APP.jinja_env.lstrip_blocks = True


def load_blueprints() -> None:
  """Attach the blueprints to the app."""
  # Views are registered to the API blueprint as a side-effect of this import.
  from ..views import all_views  # pylint: disable=unused-variable

  # Only register the /quitquitquitz handler in debug mode.
  if APP.config['DEBUG']:
    from ..views import testing  # pylint: disable=unused-variable

  APP.register_blueprint(api.API)


def configure_app(environment: 'Optional[str]' = None) -> bool:
  """Run all the configuration steps to set up the app."""
  if not load_config(environment):
    return False

  configure_jinja2()
  load_blueprints()
  DB.init_app(APP)

  return True
