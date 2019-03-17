"""Views for handling tasks."""

import typing

from ..database import db
from ..util import api
from ..util import errors as util_errors

# pylint: disable=unused-import,ungrouped-imports,invalid-name
if typing.TYPE_CHECKING:
  from typing import (
      Dict,
  )
  from ..database import models
  from ..util import auth
  from ..util import settings
# pylint: enable=unused-import,ungrouped-imports,invalid-name


SET_SETTING_WHITELIST = set([
    # Fields
    'name',
    'email',
    # Settings
    'deletion_behaviour',
    'language',
])


@api.endpoint('/get_settings')
def get_settings(token: 'auth.JWT') -> 'models.User':
  """Get all settings for the bearer of the given token."""
  return token.user


@api.endpoint('/set_setting')
def set_setting(
    token: 'auth.JWT',
    key: str,
    value: 'settings.Value'
    ) -> 'Dict[None, None]':
  """Set a setting for the bearer of the given token."""
  if key not in SET_SETTING_WHITELIST:
    raise util_errors.APIError(
        'Cannot set setting {}'.format(key), 400)

  setattr(token.user, key, value)

  db.DB.session.commit()

  return {}
