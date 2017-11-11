"""An environment configuration."""

import logging

# General app config

LOG_LEVEL = logging.DEBUG
DEBUG = True

# SQLAlchemy

SQLALCHEMY_DATABASE_URI = (
    'postgresql+pygresql://<user>:<password>@localhost:5432/<database>'
)
