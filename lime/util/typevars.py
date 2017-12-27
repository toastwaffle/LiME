"""Type variables used throughout."""

# pylint: disable=unused-import,invalid-name

from typing import (
    Any,
    Dict,
    Type,
    Union,
)

from ..database import models

Serialized = Union[Dict[str, Any], str]
Serializable = Any

# All models
Models = Union[
    models.Setting,
    models.Tag,
    models.TagGroup,
    models.Task,
    models.User
]

# Models which have an owner or user field
OwnedModels = Union[
    models.Setting,
    models.Tag,
    models.TagGroup,
    models.Task
]

ObjectID = int
