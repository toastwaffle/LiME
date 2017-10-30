"""Views for handling tasks."""

from ..database import db
from ..database import errors as db_errors
from ..database import models
from ..util import api
from ..util import auth
from ..util import errors as util_errors


def tags_from_groups(groups):
  for group in groups:
    yield from group.tags


@api.endpoint('/get_tags_and_groups')
def get_tags_and_groups(token):
  groups = list(token.user.tag_groups.all())

  return {
    'groups': groups,
    'tags': list(tags_from_groups(groups)),
  }


@api.endpoint('/add_tag_group')
def add_tag_group(token, title):
  group = models.TagGroup(owner=token.user, title=title)

  db.DB.session.add(group)
  db.DB.session.commit()

  return [group]


@api.endpoint('/add_tag')
def add_tag(token, title, group_id):
  group = models.TagGroup.get_by(object_id=group_id)
  auth.check_owner(token, 'add tag', group)

  mutated = [group]

  try:
    before = models.Tag.get_by(group_id=group_id, after=None)

    mutated.append(before)
  except db_errors.ObjectNotFoundError:
    before = None

  tag = models.Tag(group=group, title=title, before=before)

  db.DB.session.add(tag)
  db.DB.session.commit()

  mutated.append(tag)

  return [m for m in set(mutated) if m is not None]


