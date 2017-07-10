"""Enum definitions for settings."""

import enum


class NameEnum(enum.Enum):
    def _generate_next_value_(name, unused_start, unused_count,
                              unused_last_values):
        return name


class LowercaseNameEnum(enum.Enum):
    def _generate_next_value_(name, unused_start, unused_count,
                              unused_last_values):
        return name.lower()


class DeletionBehaviour(NameEnum):
  ASK = enum.auto()
  CASCADE = enum.auto()
  REPARENT = enum.auto()


class Language(LowercaseNameEnum):
  EN_GB = enum.auto()
