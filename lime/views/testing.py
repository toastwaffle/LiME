"""Utility endpoints for testing."""

import flask

from .. import app


@app.APP.route('/quitquitquitz', methods=['POST'])
def quitquitquitz():
  """Post to /quitquitquitz to shutdown gracefully."""
  func = flask.request.environ.get('werkzeug.server.shutdown')
  if func is None:
    raise RuntimeError('Not running with the Werkzeug Server')
  func()

  return 'Server shutting down...'
