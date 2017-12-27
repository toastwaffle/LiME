"""Enum definitions for settings."""

import typing

import enum

# pylint: disable=unused-import,ungrouped-imports,invalid-name
if typing.TYPE_CHECKING:
  from typing import (
      List,
      Type,
      Union,
  )

  SettingsEnum = Union[
      'DeletionBehaviour',
      'Language',
  ]
  SettingsEnumType = Union[
      Type['DeletionBehaviour'],
      Type['Language'],
  ]
# pylint: enable=unused-import,ungrouped-imports,invalid-name


class NameEnum(enum.Enum):
  """Enum class which uses the constant name as the value."""
  def _generate_next_value_(  # Enums are weird! - pylint: disable=no-self-argument
      name: str,
      unused_start: int,
      unused_count: int,
      unused_last_values: 'List[str]'
      ) -> str:
    return name


class LowercaseNameEnum(enum.Enum):
  """Enum class which lowercases the constant name for the value."""
  def _generate_next_value_(  # Enums are weird! - pylint: disable=no-self-argument
      name: str,
      unused_start: int,
      unused_count: int,
      unused_last_values: 'List[str]'
      ) -> str:
    return name.lower()


class DeletionBehaviour(NameEnum):
  """What to do when a task with children is deleted."""
  ASK = enum.auto()
  CASCADE = enum.auto()
  REPARENT = enum.auto()


class Language(LowercaseNameEnum):
  """UI Language."""
  EN_GB = enum.auto()
