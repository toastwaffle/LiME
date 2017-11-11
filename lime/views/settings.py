"""Views for handling tasks."""

from ..util import api
from ..util import errors as util_errors


SET_SETTING_WHITELIST = set([
    # Fields
    'name',
    'email',
    # Settings
    'deletion_behaviour',
    'language',
])


@api.endpoint('/get_settings')
def get_settings(token):
  """Get all settings for the bearer of the given token."""
  return token.user


@api.endpoint('/set_setting')
def set_setting(token, key, value):
  """Set a setting for the bearer of the given token."""
  if key not in SET_SETTING_WHITELIST:
    raise util_errors.APIError(
        'Cannot set setting {}'.format(key), 400)

  setattr(token.user, key, value)

  return {}
