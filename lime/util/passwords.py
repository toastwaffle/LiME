"""Descriptor for setting, checking, and updating user passwords."""

import typing

from ..database import db
from .. import app

# pylint: disable=unused-import,ungrouped-imports,invalid-name
if typing.TYPE_CHECKING:
  from typing import (
      Type,
  )
  from ..database import models
# pylint: enable=unused-import,ungrouped-imports,invalid-name

class _PasswordChecker(object):
  """Helper to allow using ==/!= for checking user passwords."""

  def __init__(self, user: 'models.User') -> None:
    self.user = user

  def __eq__(self, password: str) -> bool:
    context = app.APP.config['PASSLIB_CONTEXT']

    if not context.verify(password, self.user.password_hash):
      return False

    if context.needs_update(self.user.password_hash):
      self.user.password_hash = context.hash(password)
      db.DB.session.commit()

    return True


class PasswordDescriptor(object):
  """Descriptor for checking and setting user passwords."""

  def __get__(
      self,
      user: 'models.User',
      unused_user_type: 'Type[models.User]' = None
      ) -> _PasswordChecker:
    return _PasswordChecker(user)

  def __set__(self, user: 'models.User', password: str) -> None:
    user.password_hash = app.APP.config['PASSLIB_CONTEXT'].hash(password)
