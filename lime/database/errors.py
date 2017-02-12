"""Error classes for database operations."""


class Error(Exception):
  """Generic error for all database modules."""


class ObjectNotFoundError(Exception):
  """Looking up an object failed."""
