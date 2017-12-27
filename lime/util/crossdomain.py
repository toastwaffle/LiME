"""Utility to set HTTP Access-Control headers.

Lifted from http://flask.pocoo.org/snippets/56 on 2017-03-05.
"""

import datetime
import functools
import typing

import flask

# pylint: disable=unused-import,ungrouped-imports,invalid-name
if typing.TYPE_CHECKING:
  from typing import (
      Any,
      Callable,
      List,
      Optional,
      Union,
  )
# pylint: enable=unused-import,ungrouped-imports,invalid-name


def allow(
    origins: 'List[str]',
    methods: 'Optional[List[str]]' = None,
    headers: 'Optional[List[str]]' = None,
    max_age: int = 21600,
    attach_to_all: bool = True,
    automatic_options: bool = True) -> 'Callable[[Callable], Callable]':
  """Create a decorator to allow cross-domain requests using Access-Control."""
  origins = ', '.join(origins)

  if methods is not None:
    methods = ', '.join(sorted(x.upper() for x in methods))

  if headers is not None:
    headers = ', '.join(x.upper() for x in headers)

  if isinstance(max_age, datetime.timedelta):
    max_age = max_age.total_seconds()

  def get_methods() -> 'List[str]':
    """Get allowed HTTP methods for Access-Control-Allow-Methods."""
    if methods is not None:
      return methods

    options_resp = flask.current_app.make_default_options_response()
    return options_resp.headers['allow']

  def decorator(f: 'Callable') -> 'Callable':
    """The decorator."""
    def wrapped_function(*args: 'Any', **kwargs: 'Any'):
      """The wrapped function."""
      if automatic_options and flask.request.method == 'OPTIONS':
        resp = flask.current_app.make_default_options_response()
      else:
        resp = flask.make_response(f(*args, **kwargs))

      if not attach_to_all and flask.request.method != 'OPTIONS':
        return resp

      h = resp.headers

      h['Access-Control-Allow-Origin'] = origins
      h['Access-Control-Allow-Methods'] = get_methods()
      h['Access-Control-Max-Age'] = str(max_age)
      if headers is not None:
        h['Access-Control-Allow-Headers'] = headers
      return resp

    f.provide_automatic_options = False
    return functools.update_wrapper(wrapped_function, f)
  return decorator
