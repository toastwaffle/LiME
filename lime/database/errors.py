"""Error classes for database operations."""


class Error(Exception):
  """Parent of all DB errors."""


class ObjectNotFoundError(Exception):
  """Looking up an object failed."""
