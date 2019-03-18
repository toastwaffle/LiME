"""Default/enivronment-independent configuration."""

import datetime

from passlib import context

# General app config

SECRET_KEY: bytes = (
    b'\x14\xe7\x07P"\xb9\xbf\x94\xc0\xc9\xe0\xc2[\xd0\x92D[+\x10\xdem\xcb\x14g')
SEND_FILE_MAX_AGE_DEFAULT: int = 1209600
PREFERRED_URL_SCHEME: str = 'https'

# SQLAlchemy

SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
SQLALCHEMY_POOL_RECYCLE: int = 300

# JWT

JWT_SECRET: bytes = (
    b'O\xf1\xe4V+\x89\xf5\xcb\x95\xb2\x97\xc7\x97\x14\xa6|\xd85VJ\xb2(\xd3v')
JWT_ALGORITHM: str = 'HS512'
JWT_EXPIRY: datetime.timedelta = datetime.timedelta(days=30)
JWT_ISSUER: str = 'LiME'

# Passlib

PASSLIB_CONTEXT: context.CryptContext = context.CryptContext(
    schemes=['bcrypt'], deprecated='auto')
