"""Views for handling tasks."""

from ..util import api


@api.endpoint('/get_settings')
def get_settings(token):
  """Get all settings for the bearer of the given token."""
  return token.user.settings


@api.endpoint('/set_setting')
def set_setting(token, key, value):
  """Set a setting for the bearer of the given token."""
  setattr(token.user.settings, key, value)

  return {}
