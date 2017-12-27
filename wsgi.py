"""WSGI wrapper for LiME."""

import logging
import os
import site
import sys

from newrelic import agent

from lime import app
from lime.system import setup

APP = app.APP

agent.initialize()

# newrelic sets up its own handler to push things to stderr, we want to prevent
# the messages reaching the root logger and being duplicated
logging.getLogger('newrelic').propagate = False

setup.configure_app(os.environ['LIME_CONFIG'])

application = agent.wsgi_application()(APP)
