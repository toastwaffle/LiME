"""Helpers for handling user settings."""

import enum

from . import api
from . import errors
from . import settings_enums as enums
from ..database import db
from ..database import models
from ..database import setting


_TYPE_MAP = {
  int: setting.SettingType.INT,
  float: setting.SettingType.FLOAT,
  str: setting.SettingType.STRING,
  bool: setting.SettingType.BOOL,
}


def _check_value_type(value, expected_type):
  if value is not None and not isinstance(value, expected_type):
    raise TypeError('{} is not an instance of {}'.format(
        value, expected_type))


class _Descriptor(object):
  """Parent type for all descriptors used for settings.

  Supports enumeration in SettingManager.to_json.
  """


class UserFieldDescriptor(_Descriptor):
  """Defines a setting which is stored as a field on the User object."""

  def __init__(self, vtype):
    self.key = None
    self.vtype = vtype

  def __set_name__(self, unused_manager_type, name):
    self.key = name

  def __get__(self, manager, unused_manager_type=None):
    return getattr(manager.user, self.key)

  def __set__(self, manager, value):
    _check_value_type(value, self.vtype)

    setattr(manager.user, self.key, value)
    db.DB.session.commit()


class SettingDescriptor(_Descriptor):
  """Defines a setting with the given type and optional default value.

  This class creates a database Setting object when setting a previously unset
  setting.
  """

  def __init__(self, vtype, default=None):
    _check_value_type(default, vtype)

    self.key = None
    self.vtype = vtype
    self.default = default

  def __set_name__(self, unused_manager_type, name):
    self.key = name

  def __get__(self, manager, unused_manager_type=None):
    try:
      return manager.settings[self.key].value
    except KeyError:
      return self.default

  def __set__(self, manager, val):
    _check_value_type(val, self.vtype)

    try:
      setting = manager.settings[self.key]
    except KeyError:
      setting = models.Setting(
          user=manager.user,
          key=self.key,
          setting_type=_TYPE_MAP[self.vtype])
      manager.settings[self.key] = setting
      db.DB.session.add(setting)

    setting.value = val
    db.DB.session.commit()


def _check_enum(enum_class):
  """Asserts that an enum uses a valid type consistently.

  Returns:
    The underlying type of enum values.
  """
  if not issubclass(enum_class, enum.Enum):
    raise TypeError('{} is not an Enum'.format(enum_class))

  instances = list(enum_class)
  enum_type = type(instances[0].value)

  for instance in instances:
    if type(instance.value) is not enum_type:
      raise TypeError('enum {} uses mixed types {} and {}'.format(
        enum_class, enum_type, type(instance)))

  if enum_type not in _TYPE_MAP:
    raise TypeError(
        '{} (underlying type of {}) is not a valid setting type'.format(
            enum_type, enum_class))

  return enum_type


class EnumDescriptor(SettingDescriptor):
  """Defines an enum setting with an optional default value.

  Converts to and from the enum's underlying type.
  """

  def __init__(self, enum_class, enum_default=None):
    self.enum_type = _check_enum(enum_class)
    _check_value_type(enum_default, enum_class)
    default = None
    if enum_default is not None:
      default = enum_default.value

    super(EnumDescriptor, self).__init__(self.enum_type, default)
    self.enum_class = enum_class

  def __get__(self, manager, manager_type=None):
    value = super(EnumDescriptor, self).__get__(manager, manager_type)
    if value != None:
      return self.enum_class(value)
    return None

  def __set__(self, manager, value):
    if isinstance(value, self.enum_class):
      super(EnumDescriptor, self).__set__(manager, value.value)
    else:
      _check_value_type(value, self.enum_type)
      try:
        _ = self.enum_class(value)
      except ValueError as err:
        raise errors.APIError(err.args[0], 400)
      super(EnumDescriptor, self).__set__(manager, value)


@api.register_serializable()
class SettingsManager(object):
  """Helper class for handling user settings."""

  name = UserFieldDescriptor(str)
  email = UserFieldDescriptor(str)
  deletion_behaviour = EnumDescriptor(enums.DeletionBehaviour,
                                      enums.DeletionBehaviour.ASK)
  language = EnumDescriptor(enums.Language, enums.Language.EN_GB)

  def __init__(self, user):
    self.user = user
    self.settings = {
      setting.key: setting
      for setting in user._settings.all()
    }

  def to_json(self):
    return {
        name: getattr(self, name)
        for name, attr in SettingsManager.__dict__.items()
        if isinstance(attr, _Descriptor)
    }
