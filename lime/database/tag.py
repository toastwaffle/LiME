"""Model for tags."""

import typing

import sqlalchemy

from . import db
from ..util import api

# pylint: disable=unused-import,ungrouped-imports,invalid-name
if typing.TYPE_CHECKING:
  from typing import (
      List,
      Optional,
  )
  from . import user
  from ..util import typevars
# pylint: enable=unused-import,ungrouped-imports,invalid-name

DB = db.DB


ORDERING_LINK = DB.Table(
    'tag_ordering_link',
    DB.Model.metadata,
    DB.Column('before_id', DB.Integer, DB.ForeignKey('tag.object_id', ondelete='CASCADE')),
    DB.Column('after_id', DB.Integer, DB.ForeignKey('tag.object_id', ondelete='CASCADE'))
)


TAG_TASK_LINK = DB.Table(
    'tag_task_link',
    DB.Model.metadata,
    DB.Column('tag_id', DB.Integer, DB.ForeignKey('tag.object_id', ondelete='CASCADE')),
    DB.Column('task_id', DB.Integer, DB.ForeignKey('task.object_id', ondelete='CASCADE'))
)


@api.register_serializable()
class Tag(DB.Model):
  """Model for tags."""
  __tablename__ = 'tag'
  __json_fields__ = [
      # Fields
      'title',
      # Relation IDs
      'group_id',
      'owner_id',
      # Properties
      'before_id',
      'after_id',
  ]
  __table_args__ = (
      sqlalchemy.CheckConstraint(
          '(group_id IS NOT NULL) <> (owner_id IS NOT NULL)',
          name='has_owner_xor_group'),
  )

  # Fields
  title = DB.Column(DB.Unicode(200), nullable=False)

  # Relation IDs
  owner_id = DB.Column(
      DB.Integer(), DB.ForeignKey('user.object_id', ondelete="CASCADE"),
      nullable=True)
  group_id = DB.Column(
      DB.Integer(), DB.ForeignKey('tag_group.object_id', ondelete="CASCADE"),
      nullable=True)

  # Relations
  direct_owner = DB.relationship(
      'User',
      backref=DB.backref(
          'tags',
          lazy='dynamic',
          passive_deletes='all'
      ),
      foreign_keys=[owner_id]
  )
  group = DB.relationship(
      'TagGroup',
      backref=DB.backref(
          'tags',
          lazy='joined',
          passive_deletes='all'
      ),
      foreign_keys=[group_id]
  )
  after = DB.relationship(
      'Tag',
      backref=DB.backref(
          'before',
          uselist=False,
          lazy='joined',
          join_depth=1
      ),
      secondary=ORDERING_LINK,
      primaryjoin="Tag.object_id == tag_ordering_link.c.before_id",
      secondaryjoin="Tag.object_id == tag_ordering_link.c.after_id",
      uselist=False,
      lazy='joined',
      join_depth=1
  )
  tasks = DB.relationship(
      'Task',
      backref=DB.backref(
          'tags',
          lazy='joined'
      ),
      secondary=ORDERING_LINK,
      lazy='dynamic'
  )

  @property
  def owner(self) -> 'user.User':
    """Get the owner of this tag.

    Tags in groups maintain ownership via the enclosing group; standalone tags
    use the tag's own `owner` relation.
    """
    return self.group.owner if self.group is not None else self.direct_owner

  @property
  def before_id(self) -> 'Optional[typevars.ObjectID]':
    """The the object ID of the preceding tag in the group."""
    return self.before.object_id if self.before is not None else None

  @property
  def after_id(self) -> 'Optional[typevars.ObjectID]':
    """The the object ID of the following tag in the group."""
    return self.after.object_id if self.after is not None else None
