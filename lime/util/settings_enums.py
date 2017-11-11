"""Enum definitions for settings."""

import enum


class NameEnum(enum.Enum):
  """Enum class which uses the constant name as the value."""
  def _generate_next_value_(name, unused_start, unused_count,  # Enums are weird! - pylint: disable=no-self-argument
                            unused_last_values):
    return name


class LowercaseNameEnum(enum.Enum):
  """Enum class which lowercases the constant name for the value."""
  def _generate_next_value_(name, unused_start, unused_count,  # Enums are weird! - pylint: disable=no-self-argument
                            unused_last_values):
    return name.lower()


class DeletionBehaviour(NameEnum):
  """What to do when a task with children is deleted."""
  ASK = enum.auto()
  CASCADE = enum.auto()
  REPARENT = enum.auto()


class Language(LowercaseNameEnum):
  """UI Language."""
  EN_GB = enum.auto()
