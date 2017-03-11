"""Model for tasks."""

from . import db

DB = db.DB


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
