"""Utility to set HTTP Access-Control headers.

Lifted from http://flask.pocoo.org/snippets/56 on 2017-03-05.
"""

import datetime
import functools

import flask


def allow(origin, methods=None, headers=None, max_age=21600,
          attach_to_all=True, automatic_options=True):
  """Create a decorator to allow cross-domain requests using Access-Control."""
  if not isinstance(origin, (str, bytes)):
    origin = ', '.join(origin)

  if methods is not None:
    methods = ', '.join(sorted(x.upper() for x in methods))

  if headers is not None and not isinstance(headers, (str, bytes)):
    headers = ', '.join(x.upper() for x in headers)

  if isinstance(max_age, datetime.timedelta):
    max_age = max_age.total_seconds()

  def get_methods():
    """Get allowed HTTP methods for Access-Control-Allow-Methods."""
    if methods is not None:
      return methods

    options_resp = flask.current_app.make_default_options_response()
    return options_resp.headers['allow']

  def decorator(f):
    """The decorator."""
    def wrapped_function(*args, **kwargs):
      """The wrapped function."""
      if automatic_options and flask.request.method == 'OPTIONS':
        resp = flask.current_app.make_default_options_response()
      else:
        resp = flask.make_response(f(*args, **kwargs))

      if not attach_to_all and flask.request.method != 'OPTIONS':
        return resp

      h = resp.headers

      h['Access-Control-Allow-Origin'] = origin
      h['Access-Control-Allow-Methods'] = get_methods()
      h['Access-Control-Max-Age'] = str(max_age)
      if headers is not None:
        h['Access-Control-Allow-Headers'] = headers
      return resp

    f.provide_automatic_options = False
    return functools.update_wrapper(wrapped_function, f)
  return decorator
