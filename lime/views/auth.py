"""Views for authentication."""

from sqlalchemy import exc as sqlalchemy_exc

from ..database import db
from ..database import errors as db_errors
from ..database import models
from ..util import api
from ..util import auth
from ..util import errors as util_errors


@api.endpoint('/login', require_auth=False)
def login(email, password):
  """Login the user, and return a JSON Web Token."""
  try:
    user = models.User.get_by(email=email)
  except db_errors.ObjectNotFoundError:
    raise util_errors.APIError('Invalid email address.', 401)

  if user.password != password:
    raise util_errors.APIError('Invalid password.', 401)

  return auth.JWT.from_user(user)


@api.endpoint('/register', require_auth=False)
def register(name, email, password):
  """Create a new user, and return a JSON Web Token."""
  user = models.User(name=name, email=email, password=password)

  db.DB.session.add(user)

  try:
    db.DB.session.commit()
  except sqlalchemy_exc.IntegrityError:
    db.DB.session.rollback()
    raise util_errors.APIError('Email address already in use.', 400)

  return auth.JWT.from_user(user)
