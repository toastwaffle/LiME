"""Base table schema to reduce duplication."""

import flask_sqlalchemy
import sqlalchemy

from . import errors


class CustomModel(flask_sqlalchemy.Model):
  """Base table schema to reduce duplication."""
  __tablename__ = None

  object_id = sqlalchemy.Column(
      sqlalchemy.Integer(),
      primary_key=True,
      nullable=False
  )

  def __init__(self, **kwargs):
    for key, value in kwargs.items():
      setattr(self, key, value)

  def __repr__(self):
    return '<{0}({1})>'.format(self.__class__.__name__, self.object_id)

  @classmethod
  def get_by(cls, **predicates):
    """Get an object by a unique database field."""
    item = cls.query.filter_by(**predicates).first()

    if not item:
      raise errors.ObjectNotFoundError(
          'No {name} found satisfying {predicates}'.format(
              name=cls.__name__,
              predicates=predicates))

    return item

  def to_json(self):
    """Converts the model to a JSON serializable dictionary.

    Relies on the __json_fields__ attribute on the model class; we let the
    AttributeError stop JSON encoding if it or other attributes are not found.
    """
    return {
        key: getattr(self, key)
        for key in self.__json_fields__ + ['object_id']
    }
