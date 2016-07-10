# coding: utf-8
"""Create the SQLAlchemy connection object."""

import flask_sqlalchemy

from .. import app

# The config isn't loaded when the database object is created. Setting this
# configuration value suppresses a warning given by SQLAlchemy.
app.APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DB = flask_sqlalchemy.SQLAlchemy(app.APP)
