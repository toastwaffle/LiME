"""Error classes for utility modules."""


class Error(Exception):
  """Generic error for utility modules."""


class AuthenticationError(Error):
  """Raised when user is not authenticated or authentication is invalid."""


class SerializationError(Error):
  """Raised when there are errors in interacting with serializable objects."""


class APIError(Error):
  """Raised when handling an API call fails.

  Sends the error message and error code (a HTTP code) to the user.
  """
  def __init__(self, message, code):
    Error.__init__(self, message)

    self.code = code
