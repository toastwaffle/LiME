"""Setup for testing."""

import contextlib

from lime import app
from lime.database import db
from lime.system import setup


@contextlib.contextmanager
def test_setup():
  """Setup the app in testing mode."""
  client = app.APP.test_client()

  with app.APP.app_context():
    setup.configure_app('testing')
    db.DB.create_all()
    yield client
