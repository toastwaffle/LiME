"""Handlers for JSON based API endpoints."""

import functools
import json

import flask

from . import crossdomain
from . import errors


_SERIALIAZABLE_CLASSES_BY_CLASS = {}
_SERIALIAZABLE_CLASSES_BY_IDENTIFIER = {}

API = flask.Blueprint('api', 'api')


def register_serializable(_identifier=None):
  """Make a decorator to register a class as JSON serialiazable."""
  def decorator(cls):
    """The decorator."""
    identifier = _identifier or cls.__name__

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
  def default(self, obj):
    """Convert a serializable class to a dict to be encoded into JSON."""
    try:
      identifier = _SERIALIAZABLE_CLASSES_BY_CLASS[obj.__class__]
      return dict(obj.to_json(), __identifier=identifier)
    except KeyError:
      return json.JSONEncoder.default(self, obj)


ENCODER = Encoder()


def from_dict(data):
  """Convert a dict deserialized from JSON to the serializable class."""
  if '__identifier' in data:
    try:
      cls = _SERIALIAZABLE_CLASSES_BY_IDENTIFIER[data['__identifier']]
      return cls.from_json(data)
    except KeyError:
      pass

  return data


def endpoint(path, require_auth=True, discard_token=False):
  """Create a decorator for API methods.

  Reads POSTed JSON payload, decodes it, and passes the decoded data as kwargs
  to the wrapped function. Handles authentication, requiring an authentication
  token by default.
  """
  def parse_request():
    try:
      return json.loads(flask.request.data, object_hook=from_dict)
    except json.JSONDecodeError as err:
      raise errors.APIError('Could not parse request: {}'.format(err), 400)

  def check_auth(request):
    if 'token' not in request:
      raise errors.APIError('No authentication token provided.', 401)

    try:
      request['token'].check_valid()
    except errors.AuthenticationError as err:
      raise errors.APIError('Authentication token not valid: {}'.format(err),
                            401)
    except AttributeError as err:
      raise errors.APIError(
          'Could not parse authentication token: {}'.format(err), 401)

  def wrap(func):
    @functools.wraps(func)
    def wrapped():
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

  def decorator(func):
    return API.route(path, methods=['POST', 'OPTIONS'])(
      crossdomain.allow(origin='*', headers=['Content-Type', 'Accept'])(
        wrap(func)))

  return decorator
