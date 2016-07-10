# coding: utf-8
"""Script to run bpython with the appropriate env."""

import flask_script
from bpython import curtsies

from lime import app
from lime.database import db
from lime.database import models

class BpythonCommand(flask_script.Command):
  """Flask-Script command for running bpython with the appropriate env."""

  help = 'Run bpython in the given environment'

  @staticmethod
  def run(): # false positive pylint: disable=method-hidden
    """Call the bpython main loop

    Starts bpython with the app, database and models as local variables.
    """

    curtsies.main([], {'APP': app.APP, 'DB': db.DB, 'models': models})
