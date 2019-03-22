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


_MAX_AGE = '21600'


def allow(
    origins: 'List[str]',
    headers: 'List[str]') -> 'Callable[[Callable], Callable]':
  """Create a decorator to allow cross-domain requests using Access-Control."""
  origins = ', '.join(origins)
  headers = ', '.join(x.upper() for x in headers)

  def decorator(f: 'Callable') -> 'Callable':
    """The decorator."""
    def wrapped_function(*args: 'Any', **kwargs: 'Any'):
      """The wrapped function."""
      opts_resp = flask.current_app.make_default_options_response()

      if flask.request.method == 'OPTIONS':
        resp = opts_resp
      else:
        resp = flask.make_response(f(*args, **kwargs))

      resp.headers['Access-Control-Allow-Origin'] = origins
      resp.headers['Access-Control-Allow-Headers'] = headers
      resp.headers['Access-Control-Allow-Methods'] = opts_resp.headers['allow']
      resp.headers['Access-Control-Max-Age'] = _MAX_AGE

      return resp

    f.provide_automatic_options = False
    return functools.update_wrapper(wrapped_function, f)
  return decorator
