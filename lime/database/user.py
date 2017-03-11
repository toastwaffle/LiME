"""Model for users."""

from . import db

DB = db.DB


class User(DB.Model):
  """Model for users."""
  __tablename__ = 'user'

  # Fields
  name = DB.Column(DB.Unicode(200), nullable=False)
  email = DB.Column(DB.Unicode(200), nullable=False, unique=True)
  password_hash = DB.Column(DB.Unicode(60), nullable=False)
