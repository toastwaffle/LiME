"""Model for users."""

from . import db

DB = db.DB


class User(DB.Model):
  """Model for users."""
  __tablename__ = 'user'

  name = DB.Column(DB.Unicode(200), nullable=False)
  email = DB.Column(DB.Unicode(200), nullable=False, unique=True)
  password_hash = DB.Column(DB.Unicode(60), nullable=False)

  def __init__(self, name, email, password_hash):
    self.name = name
    self.email = email
    self.password_hash = password_hash
