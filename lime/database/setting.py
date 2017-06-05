"""Model for user settings."""

import enum

from . import db

DB = db.DB


class SettingType(enum.Enum):
  INT = 'int_value'
  FLOAT = 'float_value'
  STRING = 'string_value'
  BOOL = 'bool_value'


class Setting(DB.Model):
  """Model for user settings."""
  __tablename__ = 'setting'

  # Fields
  key = DB.Column(DB.String(20), nullable=False)
  setting_type = DB.Column(DB.Enum(SettingType, name='setting_type'),
                           nullable=False)
  int_value = DB.Column(DB.Integer(), nullable=True)
  float_value = DB.Column(DB.Float(), nullable=True)
  string_value = DB.Column(DB.Unicode(), nullable=True)
  bool_value = DB.Column(DB.Boolean(), nullable=True)

  # Relation IDs
  user_id = DB.Column(
      DB.Integer(), DB.ForeignKey('user.object_id', ondelete="CASCADE"),
      nullable=False)

  # Relations
  user = DB.relationship(
      'User',
      backref=DB.backref(
          '_settings',
          lazy='dynamic',
          passive_deletes='all'
      ),
      foreign_keys=[user_id]
  )

  @property
  def value(self):
    return getattr(self, self.setting_type.value)

  @value.setter
  def value(self, val):
    return setattr(self, self.setting_type.value, val)
