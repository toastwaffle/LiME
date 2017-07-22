"""Model for tasks."""

import sqlalchemy

from . import db
from ..util import api

DB = db.DB


ORDERING_LINK = DB.Table(
    'ordering_link',
    DB.Model.metadata,
    DB.Column('before_id', DB.Integer, DB.ForeignKey('task.object_id')),
    DB.Column('after_id', DB.Integer, DB.ForeignKey('task.object_id'))
)


@api.register_serializable()
class Task(DB.Model):
  """Model for tasks."""
  __tablename__ = 'task'

  # Fields
  title = DB.Column(DB.Unicode(200), nullable=False)
  completed = DB.Column(DB.Boolean(), nullable=False, default=False)

  # Relation IDs
  owner_id = DB.Column(
      DB.Integer(), DB.ForeignKey('user.object_id', ondelete="CASCADE"),
      nullable=False)
  parent_id = DB.Column(
      DB.Integer(),
      DB.ForeignKey('task.object_id', ondelete="CASCADE"),
      nullable=True)

  # Relations
  owner = DB.relationship(
      'User',
      backref=DB.backref(
          'tasks',
          lazy='dynamic',
          passive_deletes='all'
      ),
      foreign_keys=[owner_id]
  )
  parent = DB.relationship(
      'Task',
      backref=DB.backref(
          'children',
          lazy='dynamic',
          passive_deletes='all'
      ),
      foreign_keys=[parent_id],
      remote_side='Task.object_id'
  )
  after = DB.relationship(
      'Task',
      backref=DB.backref(
          'before',
          uselist=False,
          lazy='joined',
          join_depth=1
      ),
      secondary=ORDERING_LINK,
      primaryjoin="Task.object_id == ordering_link.c.before_id",
      secondaryjoin="Task.object_id == ordering_link.c.after_id",
      uselist=False,
      lazy='joined',
      join_depth=1
  )

  @property
  def has_children(self):
    return DB.session.query(
        sqlalchemy.literal(True)
    ).filter(
        self.children.exists()
    ).scalar()

  def to_json(self):
    """Converts the task to a JSON serializable object."""
    before_id = self.before.object_id if self.before is not None else None
    after_id = self.after.object_id if self.after is not None else None
    return {
        'object_id': self.object_id,
        'owner_id': self.owner_id,
        'parent_id': self.parent_id,
        'title': self.title,
        'completed': self.completed,
        'has_children': self.has_children,
        'before_id': before_id,
        'after_id': after_id,
    }
