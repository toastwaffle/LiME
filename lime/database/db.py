"""Create the SQLAlchemy connection object."""

import flask_sqlalchemy

from . import custom_model

DB = flask_sqlalchemy.SQLAlchemy(model_class=custom_model.CustomModel)
