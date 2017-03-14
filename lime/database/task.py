"""Model for tasks."""

from . import db
from ..util import api

DB = db.DB


@api.register_serializable()
class Task(DB.Model):
  """Model for tasks."""
  __tablename__ = 'task'

  # Fields
  title = DB.Column(DB.Unicode(200), nullable=False)

  # Relation IDs
  owner_id = DB.Column(
      DB.Integer(), DB.ForeignKey('user.object_id'), nullable=False)

  # Relations
  owner = DB.relationship(
      'User',
      backref=DB.backref(
          'tasks',
          lazy='dynamic'
      ),
      foreign_keys=[owner_id]
  )

  def to_json(self):
    """Converts the task to a JSON serializable object."""
    return {
        'object_id': self.object_id,
        'owner_id': self.owner_id,
        'title': self.title,
    }

