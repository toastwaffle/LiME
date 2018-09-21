"""Views for handling tasks."""

import typing

from ..database import db
from ..database import errors as db_errors
from ..database import models
from ..util import api
from ..util import auth

# pylint: disable=unused-import,ungrouped-imports,invalid-name
if typing.TYPE_CHECKING:
  from typing import (
      Dict,
      Generator,
      List,
      Optional,
      Union,
  )
  from ..util import typevars
# pylint: enable=unused-import,ungrouped-imports,invalid-name


def tags_from_groups(
    groups: 'List[models.TagGroup]'
    ) -> 'Generator[models.Tag, None, None]':
  """Generate all the tags within the given groups."""
  for group in groups:
    yield from group.tags


@api.endpoint('/get_tags_and_groups')
def get_tags_and_groups(
    token: 'auth.JWT'
    ) -> 'Dict[str, Union[List[models.TagGroup], List[models.Tag]]]':
  """Get all tags and tag groups owned by the token bearer."""
  groups = list(token.user.tag_groups.all())

  return groups + list(tags_from_groups(groups)) + list(token.user.tags.all())


@api.endpoint('/add_tag_group')
def add_tag_group(
    token: 'auth.JWT',
    title: str
    ) -> 'List[models.TagGroup]':
  """Add a new tag group."""
  group = models.TagGroup(owner=token.user, title=title)

  db.DB.session.add(group)
  db.DB.session.commit()

  return [group]


@api.endpoint('/add_tag')
def add_tag(
    token: 'auth.JWT',
    title: str,
    group_id: 'Optional[typevars.ObjectID]' = None
    ) -> 'List[models.TagGroup]':
  """Add a new tag in the given group."""
  mutated = []
  before = None

  if group_id is not None:
    owner = None
    group = models.TagGroup.get_by(object_id=group_id)
    auth.check_owner(token, 'add tag', group)

    mutated.append(group)

    try:
      before = models.Tag.get_by(group_id=group_id, after=None)

      mutated.append(before)
    except db_errors.ObjectNotFoundError:
      pass
  else:
    owner = token.user
    group = None

  tag = models.Tag(group=group, direct_owner=owner, title=title, before=before)

  db.DB.session.add(tag)
  db.DB.session.commit()

  mutated.append(tag)

  return [m for m in set(mutated) if m is not None]


@api.endpoint('/add_tag_to_tasks')
def add_tag_to_tasks(
    token: 'auth.JWT',
    tag_id: 'typevars.ObjectID',
    task_ids: 'List[typevars.ObjectID]'
    ) -> 'List[models.Task]':
  """Add a tag to tasks, enforcing mutual exclusivity of tags in groups."""
  (new_tag,) = auth.load_owned_objects(
      models.Tag, token, 'add tag to tasks', tag_id)
  tasks = auth.load_owned_objects(
      models.Task, token, 'add tag to tasks', *task_ids)

  for task in tasks:
    if new_tag.group_id is not None:
      try:
        task.tags.remove([
            tag for tag in task.tags if tag.group_id == new_tag.group_id][0])
      except IndexError:
        pass

    task.tags.append(new_tag)

  db.DB.session.commit()

  return tasks


@api.endpoint('/remove_tag_from_tasks')
def remove_tag_from_tasks(
    token: 'auth.JWT',
    tag_id: 'typevars.ObjectID',
    task_ids: 'List[typevars.ObjectID]'
    ) -> 'List[models.Task]':
  """Remove a tag from tasks."""
  (tag,) = auth.load_owned_objects(
      models.Tag, token, 'remove tag from tasks', tag_id)
  tasks = auth.load_owned_objects(
      models.Task, token, 'remove tag from tasks', *task_ids)

  for task in tasks:
    try:
      task.tags.remove(tag)
    except ValueError:
      pass

  db.DB.session.commit()

  return tasks


