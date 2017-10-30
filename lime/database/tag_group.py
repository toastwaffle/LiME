"""Model for tag groups."""

import sqlalchemy

from . import db
from ..util import api

DB = db.DB


@api.register_serializable()
class TagGroup(DB.Model):
  """Model for tag groups."""
  __tablename__ = 'tag_group'
  __json_fields__ = [
      # Fields
      'title',
      # Relation IDs
      'owner_id',
      # Properties
      'tag_ids',
  ]

  # Fields
  title = DB.Column(DB.Unicode(200), nullable=False)

  # Relation IDs
  owner_id = DB.Column(
      DB.Integer(), DB.ForeignKey('user.object_id', ondelete="CASCADE"),
      nullable=False)

  # Relations
  owner = DB.relationship(
      'User',
      backref=DB.backref(
          'tag_groups',
          lazy='dynamic',
          passive_deletes='all'
      ),
      foreign_keys=[owner_id]
  )

  @property
  def tag_ids(self):
    return [tag.object_id for tag in self.tags]
