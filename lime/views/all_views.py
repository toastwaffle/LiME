"""Proxy module to import all the view modules.

Views are registered as a side-effect of importing the view modules.
"""

# pylint: disable=unused-import

from . import auth
from . import settings
from . import tags
from . import tasks
from . import test
