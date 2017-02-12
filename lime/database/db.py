"""Create the SQLAlchemy connection object."""

import flask_sqlalchemy
from sqlalchemy.ext import declarative

from .. import app
from . import custom_model

# The config isn't loaded when the database object is created. Setting this
# configuration value suppresses a warning given by SQLAlchemy.
app.APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DB = flask_sqlalchemy.SQLAlchemy(app.APP)

# Awkward hack to use a custom model class. Flask-SQLAlchemy 3.0 (in beta as of
# 2016-01-11) has a model_class parameter to the above constructor, which should
# be used once v3.0 is released as stable.
DB.Model = declarative.declarative_base(cls=custom_model.CustomModel)
DB.Model.query = flask_sqlalchemy._QueryProperty(DB) # pylint: disable=protected-access
