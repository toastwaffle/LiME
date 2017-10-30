"""Model for tags."""

import sqlalchemy

from . import db
from ..util import api

DB = db.DB


ORDERING_LINK = DB.Table(
    'tag_ordering_link',
    DB.Model.metadata,
    DB.Column('before_id', DB.Integer, DB.ForeignKey('tag.object_id', ondelete='CASCADE')),
    DB.Column('after_id', DB.Integer, DB.ForeignKey('tag.object_id', ondelete='CASCADE'))
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
      # Properties
      'before_id',
      'after_id',
  ]

  # Fields
  title = DB.Column(DB.Unicode(200), nullable=False)

  # Relation IDs
  group_id = DB.Column(
      DB.Integer(), DB.ForeignKey('tag_group.object_id', ondelete="CASCADE"),
      nullable=False)

  # Relations
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

  @property
  def before_id(self):
    return self.before.object_id if self.before is not None else None

  @property
  def after_id(self):
    return self.after.object_id if self.after is not None else None
