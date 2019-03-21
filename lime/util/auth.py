"""Authentication using JSON Web Tokens."""

import datetime
import typing

import jwt

from .. import app
from ..database import errors as db_errors
from ..database import models
from . import api
from . import errors

# pylint: disable=unused-import,ungrouped-imports,invalid-name
if typing.TYPE_CHECKING:
  from typing import (
      Any,
      Dict,
      Optional,
      Type,
  )
  from . import typevars
# pylint: enable=unused-import,ungrouped-imports,invalid-name


APP = app.APP


@api.register_serializable()
class JWT(object):
  """Model for a JSON Web Token (RFC 7519)."""

  __slots__ = ['user_id', 'key', '_user']

  def __init__(
      self,
      user_id: int,
      key: bytes,
      user: 'Optional[models.User]' = None
      ) -> None:
    self.user_id = user_id
    self.key = key
    self._user = user

  @classmethod
  def from_user(cls, user: 'models.User') -> 'JWT':
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

  def check_valid(self) -> None:
    """Assert that the token is valid."""
    try:
      jwt.decode(self.key, APP.config['JWT_SECRET'],
                 algorithms=[APP.config['JWT_ALGORITHM']],
                 audience=str(self.user_id))
    except jwt.InvalidTokenError as err:
      raise errors.AuthenticationError(err)

  @property
  def user(self) -> 'models.User':
    """Get the user authorised by this token."""
    if self._user is None:
      try:
        self.check_valid()
        self._user = models.User.get_by(object_id=self.user_id)
      except db_errors.ObjectNotFoundError as err:
        raise errors.AuthenticationError(err)

    return self._user

  def to_json(self) -> 'typevars.Serializable':
    """Converts the token to a JSON serializable object."""
    return {
        'user_id': self.user_id,
        'key': self.key.decode(),
    }

  @classmethod
  def from_json(cls, data: 'Dict[str, Any]') -> 'JWT':
    """Create the token object from the dictionary loaded from JSON."""
    return cls(user_id=data['user_id'], key=data['key'].encode())


def check_owner(
    token: 'JWT',
    action: str,
    *objects: 'typevars.OwnedModels'
    ) -> None:
  """Check that all objects are owned by the token bearer."""
  for obj in objects:
    if obj is None:
      continue

    try:
      owner = obj.owner
    except AttributeError:
      owner = obj.user

    if owner.object_id != token.user_id:
      raise errors.APIError(
          'Could not {}; not authorized'.format(action), 403)


def load_owned_objects(
    model: 'Type[typevars.OwnedModels]',
    token: 'auth.JWT',
    action: str,
    *object_ids: 'typevars.ObjectID'
    ) -> 'List[typevars.OwnedModels]':
  """Load a set of objects by ID and check they're owned by the token bearer."""
  objects: 'List[typevars.OwnedModels]' = []

  for object_id in object_ids:
    if object_id is None:
      objects.append(None)
      continue

    try:
      objects.append(model.get_by(object_id=object_id))
    except db_errors.ObjectNotFoundError:
      raise errors.APIError(
          'Could not {0}; {1} {2} not found'.format(action, model.__name__, object_id), 410)

  check_owner(token, action, *objects)

  return objects
