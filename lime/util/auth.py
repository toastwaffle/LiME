"""Authentication using JSON Web Tokens."""

import datetime

import jwt

from .. import app
from ..database import errors as db_errors
from ..database import models
from . import api
from . import errors

APP = app.APP


@api.register_serializable()
class JWT(object):
  """Model for a JSON Web Token (RFC 7519)."""

  __slots__ = ['user_id', 'key', '_user']

  def __init__(self, user_id, key, user=None):
    self.user_id = user_id
    self.key = key
    self._user = user

  @classmethod
  def from_user(cls, user):
    """Create a token for a user."""
    now = datetime.datetime.utcnow()
    payload = {
        'iat': now,
        'nbf': now,
        'exp': now + APP.config['JWT_EXPIRY'],
        'iss': APP.config['JWT_ISSUER'],
        'aud': str(user.object_id),
    }
    key = jwt.encode(payload, APP.config['JWT_SECRET'],
                     APP.config['JWT_ALGORITHM'])
    return cls(user.object_id, key, user)

  def check_valid(self):
    try:
      jwt.decode(self.key, APP.config['JWT_SECRET'],
                 algorithms=[APP.config['JWT_ALGORITHM']],
                 audience=str(self.user_id))
    except jwt.InvalidTokenError as err:
      raise errors.AuthenticationError(err)

  @property
  def user(self):
    """Get the user authorised by this token."""
    if self._user is None:
      try:
        self.check_valid()
        self._user = models.User.get_by_object_id(self.user_id)
      except db_errors.ObjectNotFoundError as err:
        raise errors.AuthenticationError(err)

    return self._user

  def to_json(self):
    """Converts the token to a JSON serializable object."""
    return {
        'user_id': self.user_id,
        'key': self.key.decode(),
    }

  @classmethod
  def from_json(cls, data):
    return cls(user_id=data['user_id'], key=data['key'].encode())
