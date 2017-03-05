"""Views for authentication."""

from .. import app
from ..database import db
from ..database import errors as db_errors
from ..database import models
from ..util import api
from ..util import auth
from ..util import errors as util_errors


PASSLIB_CONTEXT = app.APP.config['PASSLIB_CONTEXT']


@api.endpoint('/login', require_auth=False)
def login(email, password):
  try:
    user = models.User.get_by(email=email)
  except db_errors.ObjectNotFoundError:
    raise util_errors.APIError('Invalid email address.', 401)

  if not PASSLIB_CONTEXT.verify(password, user.password_hash):
    raise util_errors.APIError('Invalid password.', 401)

  if PASSLIB_CONTEXT.needs_update(user.password_hash):
    user.password_hash = PASSLIB_CONTEXT.hash(password)
    db.DB.session.commit()

  return auth.JWT.from_user(user)


@api.endpoint('/register', require_auth=False)
def register(name, email, password):
  user = models.User(name=name, email=email,
                     password_hash=PASSLIB_CONTEXT.hash(password))

  db.DB.session.add(user)
  db.DB.session.commit()

  return auth.JWT.from_user(user)
