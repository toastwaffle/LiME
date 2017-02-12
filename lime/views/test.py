"""Test views."""

from ..util import api

@api.endpoint('/echo', discard_token=True)
def echo(message):
  return message
