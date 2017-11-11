"""Descriptor for setting, checking, and updating user passwords."""

from ..database import db
from .. import app


class _PasswordChecker(object):
  """Helper to allow using ==/!= for checking user passwords."""

  def __init__(self, user):
    self.user = user

  def __eq__(self, password):
    context = app.APP.config['PASSLIB_CONTEXT']

    if not context.verify(password, self.user.password_hash):
      return False

    if context.needs_update(self.user.password_hash):
      self.user.password_hash = context.hash(password)
      db.DB.session.commit()

    return True


class PasswordDescriptor(object):
  """Descriptor for checking and setting user passwords."""

  def __get__(self, user, unused_user_type=None):
    return _PasswordChecker(user)

  def __set__(self, user, password):
    user.password_hash = app.APP.config['PASSLIB_CONTEXT'].hash(password)
