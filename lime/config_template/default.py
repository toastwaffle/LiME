"""Default/enivronment-independent configuration."""

import datetime

from passlib import context

# General app config

SECRET_KEY: bytes = b''  # use os.urandom(24) to generate
SEND_FILE_MAX_AGE_DEFAULT: int = 1209600
PREFERRED_URL_SCHEME: str = 'https'

# SQLAlchemy

SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
SQLALCHEMY_POOL_RECYCLE: int = 300

# JWT

JWT_SECRET: bytes = b''  # use os.urandom(24) to generate
JWT_ALGORITHM: str = 'HS512'
JWT_EXPIRY: datetime.timedelta = datetime.timedelta(days=30)
JWT_ISSUER: str = 'LiME'

# Passlib

PASSLIB_CONTEXT: context.CryptContext = context.CryptContext(
    schemes=['bcrypt'], deprecated='auto')
