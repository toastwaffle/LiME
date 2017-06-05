"""Views for handling tasks."""

from ..database import db
from ..database import errors as db_errors
from ..database import models
from ..util import api
from ..util import errors as util_errors


@api.endpoint('/get_settings')
def get_settings(token):
  return token.user.settings


@api.endpoint('/set_setting')
def set_setting(token, key, value):
  setattr(token.user.settings, key, value)

  return {}
