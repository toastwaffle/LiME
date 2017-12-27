"""An environment configuration."""

import logging

# General app config

LOG_LEVEL: int = logging.DEBUG
DEBUG: bool = True

# SQLAlchemy

SQLALCHEMY_DATABASE_URI: str = (
    'postgresql+pygresql://<user>:<password>@localhost:5432/<database>'
)
