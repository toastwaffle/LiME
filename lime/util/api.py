"""Handlers for JSON based API endpoints."""

import typing

import enum
import functools
import json

import flask
from absl import logging

from . import crossdomain
from . import errors

# pylint: disable=unused-import,ungrouped-imports,invalid-name
if typing.TYPE_CHECKING:
  from typing import (
      Any,
      Callable,
      Dict,
      Optional,
      Type,
      TypeVar,
      Union,
  )
  from . import typevars
# pylint: enable=unused-import,ungrouped-imports,invalid-name

_SERIALIAZABLE_CLASSES_BY_CLASS: 'Dict[Type, str]' = {}
_SERIALIAZABLE_CLASSES_BY_IDENTIFIER: 'Dict[str, Type]' = {}

API = flask.Blueprint('api', 'api')


def register_serializable(_identifier: 'Optional[str]' = None) -> 'Callable[[Type], Type]':
  """Make a decorator to register a class as JSON serialiazable."""
  def decorator(cls: 'Type') -> 'Type':
    """The decorator."""
    identifier = _identifier or cls.__name__

    logging.debug('Registering %r as "%s"', cls, identifier)

    if not hasattr(cls, 'to_json'):
      raise errors.SerializationError(
          '{} must define a `to_json` method.'.format(cls.__name__))
    if identifier in _SERIALIAZABLE_CLASSES_BY_IDENTIFIER:
      raise errors.SerializationError(
          'Identifier "{}" is already registered.'.format(identifier))

    _SERIALIAZABLE_CLASSES_BY_IDENTIFIER[identifier] = cls
    _SERIALIAZABLE_CLASSES_BY_CLASS[cls] = identifier

    return cls

  return decorator


class Encoder(json.JSONEncoder):
  """Custom JSON encoder for registered serializable classes."""

  def default(self, o: 'typevars.Serializable') -> 'typevars.Serialized':  # Default __init__ can shadow it, but we don't - pylint: disable=method-hidden
    """Convert a serializable class to a dict to be encoded into JSON."""
    if isinstance(o, enum.Enum):
      return o.value

    try:
      identifier = _SERIALIAZABLE_CLASSES_BY_CLASS[o.__class__]
      return dict(o.to_json(), __identifier=identifier)
    except KeyError:
      return json.JSONEncoder.default(self, o)


ENCODER = Encoder()


def from_dict(data: 'Dict[str, Any]') -> 'typevars.Serializable':
  """Convert a dict deserialized from JSON to the serializable class."""
  if '__identifier' in data:
    try:
      cls = _SERIALIAZABLE_CLASSES_BY_IDENTIFIER[data['__identifier']]
      return cls.from_json(data)
    except KeyError:
      pass

  return data


def endpoint(path: str, require_auth: bool = True, discard_token: bool = False) -> 'Callable':
  """Create a decorator for API methods.

  Reads POSTed JSON payload, decodes it, and passes the decoded data as kwargs
  to the wrapped function. Handles authentication, requiring an authentication
  token by default.
  """
  def parse_request() -> 'Dict[str, Any]':
    """Parse the JSON or throw an exception."""
    try:
      return json.loads(flask.request.data, object_hook=from_dict)
    except json.JSONDecodeError as err:
      logging.exception(err)
      raise errors.APIError('Could not parse request: {}'.format(err), 400)

  def check_auth(request: 'Dict[str, Any]') -> None:
    """Check that the JSON Web Token exists and is valid."""
    if 'token' not in request:
      raise errors.APIError('No authentication token provided.', 401)

    try:
      request['token'].check_valid()
    except errors.AuthenticationError as err:
      logging.exception(err)
      raise errors.APIError('Authentication token not valid.', 401)
    except AttributeError as err:
      logging.exception(err)
      raise errors.APIError('Could not parse authentication token.', 401)

  def wrap(func: 'Callable') -> 'Callable':
    """Wrap the API function to provide JSON interface and auth checks."""
    @functools.wraps(func)
    def wrapped() -> flask.Response:
      """The wrapped function."""
      try:
        request = parse_request()

        if require_auth:
          check_auth(request)

          if discard_token:
            del request['token']

        return flask.Response(response=ENCODER.encode(func(**request)),
                              mimetype='text/json')
      except errors.APIError as err:
        return flask.Response(response=ENCODER.encode({'error': str(err)}),
                              status=err.code,
                              mimetype='text/json')

    return wrapped

  def decorator(func: 'Callable') -> 'Callable':
    """Create a decorator which sets up the route and crossdomain headers."""
    return API.route(path, methods=['POST', 'OPTIONS'])(
        crossdomain.allow(origins=['*'], headers=['Content-Type', 'Accept'])(
            wrap(func)))

  return decorator
