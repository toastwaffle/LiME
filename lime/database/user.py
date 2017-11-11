"""Model for users."""

from . import db
from ..util import settings

DB = db.DB


class User(DB.Model):
  """Model for users."""
  __tablename__ = 'user'

  # Fields
  name = DB.Column(DB.Unicode(200), nullable=False)
  email = DB.Column(DB.Unicode(200), nullable=False, unique=True)
  password_hash = DB.Column(DB.Unicode(60), nullable=False)

  @property
  def settings(self):
    """Get a SettingsManager for this user."""
    return settings.SettingsManager(self)
