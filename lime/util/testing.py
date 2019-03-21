"""Setup for testing."""

import typing

import contextlib

from lime import app
from lime.database import db
from lime.database import models
from lime.system import setup
from lime.util import api
from lime.util import auth

# pylint: disable=unused-import,ungrouped-imports,invalid-name
if typing.TYPE_CHECKING:
  from typing import (
      Any,
      Dict,
  )


@contextlib.contextmanager
def test_setup():
  """Setup the app in testing mode."""
  client = app.APP.test_client()

  with app.APP.app_context():
    setup.configure_app('testing')
    db.DB.create_all()
    yield client


def with_token(request: 'Dict[str, Any]') -> 'str':
  """Build a JSON request with a valid token."""
  return api.ENCODER.encode(
      dict(request, token=auth.JWT.from_user(models.User(object_id=1))))
