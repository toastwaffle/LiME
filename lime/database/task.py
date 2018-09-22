"""Model for tasks."""

import typing

import sqlalchemy

from . import db
from ..util import api

# pylint: disable=unused-import,ungrouped-imports,invalid-name
if typing.TYPE_CHECKING:
  from ..util import typevars
# pylint: enable=unused-import,ungrouped-imports,invalid-name

DB = db.DB


ORDERING_LINK = DB.Table(
    'task_ordering_link',
    DB.Model.metadata,
    DB.Column('before_id', DB.Integer, DB.ForeignKey('task.object_id', ondelete='CASCADE')),
    DB.Column('after_id', DB.Integer, DB.ForeignKey('task.object_id', ondelete='CASCADE'))
)


@api.register_serializable()
class Task(DB.Model):
  """Model for tasks."""
  __tablename__ = 'task'
  __json_fields__ = [
      # Fields
      'title',
      'completed',
      'notes',
      # Relation IDs
      'owner_id',
      'parent_id',
      # Properties
      'has_children',
      'before_id',
      'after_id',
      'tag_ids',
  ]

  # Fields
  title = DB.Column(DB.UnicodeText(), nullable=False)
  completed = DB.Column(DB.Boolean(), nullable=False, default=False)
  notes = DB.Column(DB.UnicodeText(), nullable=False, default='')

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
      primaryjoin="Task.object_id == task_ordering_link.c.before_id",
      secondaryjoin="Task.object_id == task_ordering_link.c.after_id",
      uselist=False,
      lazy='joined',
      join_depth=1
  )

  @property
  def has_children(self) -> bool:
    """Return whether the task has any direct children."""
    return DB.session.query(
        sqlalchemy.literal(True)
    ).filter(
        self.children.exists()
    ).scalar()

  @property
  def before_id(self) -> 'typevars.ObjectID':
    """Indirect to the object ID of the preceding task, or None."""
    return self.before.object_id if self.before is not None else None

  @property
  def after_id(self) -> 'typevars.ObjectID':
    """Indirect to the object ID of the following task, or None."""
    return self.after.object_id if self.after is not None else None

  @property
  def tag_ids(self) -> 'List[typevars.ObjectID]':
    """The the object ID of the following tag in the group."""
    return [tag.object_id for tag in self.tags]
