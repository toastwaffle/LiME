"""Model for users."""

from . import db
from ..util import api
from ..util import settings
from ..util import settings_enums

DB = db.DB


@api.register_serializable()
class User(DB.Model):
  """Model for users."""
  __tablename__ = 'user'
  __json_fields__ = [
      # Fields
      'name',
      'email',
      # Settings
      'deletion_behaviour',
      'language',
  ]

  # Fields
  name = DB.Column(DB.Unicode(200), nullable=False)
  email = DB.Column(DB.Unicode(200), nullable=False, unique=True)
  password_hash = DB.Column(DB.Unicode(60), nullable=False)

  # Settings
  deletion_behaviour = settings.EnumDescriptor(
      settings_enums.DeletionBehaviour, settings_enums.DeletionBehaviour.ASK)
  language = settings.EnumDescriptor(
      settings_enums.Language, settings_enums.Language.EN_GB)

  def get_setting(self, key):
    """Get a setting by key.

    Settings are eagerly loaded to save DB queries, but making a reusable dict
    of settings is non-trivial. Instead, we do a linear search over the list.
    """
    for setting in self.settings:
      if setting.key == key:
        return setting

    raise KeyError('No setting found with key {}'.format(key))
