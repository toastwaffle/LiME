"""Descriptors and helpers for handling user settings.

Intended to avoid an explosion of columns on the user object.
"""

import typing

import enum

from . import errors
from ..database import db
from ..database import setting as db_setting

# pylint: disable=unused-import,ungrouped-imports,invalid-name
if typing.TYPE_CHECKING:
  from typing import (
      List,
      Optional,
      Type,
      Union,
  )
  from . import settings_enums
  from ..database import user

  Scalar = Union[
      int,
      float,
      str,
      bool,
  ]
  ScalarTypes = Union[
      Type[int],
      Type[float],
      Type[str],
      Type[bool],
  ]
  Value = Union[
      int,
      float,
      str,
      bool,
      settings_enums.SettingsEnum,
  ]
  ValueType = Union[
      ScalarTypes,
      settings_enums.SettingsEnumType,
  ]
# pylint: enable=unused-import,ungrouped-imports,invalid-name


_TYPE_MAP = {
    int: db_setting.SettingType.INT,
    float: db_setting.SettingType.FLOAT,
    str: db_setting.SettingType.STRING,
    bool: db_setting.SettingType.BOOL,
}


def _check_value_type(value: 'Value', expected_type: 'ValueType') -> None:
  if value is not None and not isinstance(value, expected_type):
    raise TypeError('{} is not an instance of {}'.format(
        value, expected_type))


class SettingDescriptor(object):
  """Defines a setting with the given type and optional default value.

  This class creates a database Setting object when setting a previously unset
  setting.
  """

  def __init__(
      self,
      vtype: 'ScalarTypes',
      default: 'Optional[Scalar]' = None
      ) -> None:
    _check_value_type(default, vtype)

    self.key = None
    self.vtype = vtype
    self.default = default

  def __set_name__(
      self,
      unused_user_type: 'Type[user.User]',
      name: str
      ) -> None:
    self.key = name

  def __get__(
      self,
      owner: 'user.User',
      unused_user_type: 'Optional[Type[user.User]]' = None
      ) -> 'Scalar':
    try:
      return owner.get_setting(self.key).value
    except KeyError:
      return self.default

  def __set__(
      self,
      owner: 'user.User',
      val: 'Scalar'
      ) -> None:
    _check_value_type(val, self.vtype)

    try:
      setting = owner.get_setting(self.key)
    except KeyError:
      setting = db_setting.Setting(
          user=owner,
          key=self.key,
          setting_type=_TYPE_MAP[self.vtype])
      db.DB.session.add(setting)

    setting.value = val
    db.DB.session.commit()


def _check_enum(
    enum_class: 'settings_enums.SettingsEnumType'
    ) -> 'ScalarTypes':
  """Asserts that an enum uses a valid type consistently.

  Returns:
    The underlying type of enum values.
  """
  if not issubclass(enum_class, enum.Enum):
    raise TypeError('{} is not an Enum'.format(enum_class))

  instances: 'List[settings_enums.SettingsEnum]' = list(enum_class)
  enum_type = type(instances[0].value)

  for instance in instances:
    if not isinstance(instance.value, enum_type):
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

  def __init__(
      self,
      enum_class: 'settings_enums.SettingsEnumType',
      enum_default: 'Optional[settings_enums.SettingsEnum]' = None
      ) -> None:
    self.enum_type = _check_enum(enum_class)
    _check_value_type(enum_default, enum_class)
    default = None
    if enum_default is not None:
      default = enum_default.value

    super(EnumDescriptor, self).__init__(self.enum_type, default)
    self.enum_class = enum_class

  def __get__(
      self,
      owner: 'user.User',
      user_type: 'Type[user.User]' = None
      ) -> 'Optional[settings_enums.SettingsEnum]':
    value = super(EnumDescriptor, self).__get__(owner, user_type)
    if value != None:
      return self.enum_class(value)
    return None

  def __set__(
      self,
      owner: 'user.User',
      value: 'Value'
      ) -> None:
    if isinstance(value, self.enum_class):
      super(EnumDescriptor, self).__set__(owner, value.value)
    else:
      _check_value_type(value, self.enum_type)
      try:
        _ = self.enum_class(value)
      except ValueError as err:
        raise errors.APIError(err.args[0], 400)
      super(EnumDescriptor, self).__set__(owner, value)
