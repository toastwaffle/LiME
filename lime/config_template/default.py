"""Default/enivronment-independent configuration."""

import datetime

from passlib import context

# General app config

SECRET_KEY = ''  # use os.urandom(24) to generate
SEND_FILE_MAX_AGE_DEFAULT = 1209600
PREFERRED_URL_SCHEME = 'https'

# SQLAlchemy

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 300

# JWT

JWT_SECRET = ''  # use os.urandom(24) to generate
JWT_ALGORITHM = 'HS512'
JWT_EXPIRY = datetime.timedelta(days=30)
JWT_ISSUER = 'LiME'

# Passlib

PASSLIB_CONTEXT = context.CryptContext(schemes=['bcrypt'], deprecated='auto')
