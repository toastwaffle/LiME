"""Views for handling tasks."""

import typing

from ..database import db
from ..database import errors as db_errors
from ..database import models
from ..util import api
from ..util import auth
from ..util import errors as util_errors

# pylint: disable=unused-import,ungrouped-imports,invalid-name
if typing.TYPE_CHECKING:
  from typing import (
      Any,
      List,
      Optional,
  )
  from ..util import typevars
# pylint: enable=unused-import,ungrouped-imports,invalid-name


def check_reparent(
    task: 'models.Task',
    new_parent: 'models.Task'
    ) -> None:
  """Reparent a task, checking for cycles."""
  parent = new_parent

  while parent is not None:
    if task is parent:
      raise util_errors.APIError(
          'Cannot make task its own descendant', 400)
    parent = parent.parent

  task.parent = new_parent


@api.endpoint('/get_tasks')
def get_tasks(
    token: 'auth.JWT',
    parent_id: 'Optional[typevars.ObjectID]' = None
    ) -> 'List[models.Task]':
  """Get all direct child tasks of the given parent.

  We load the parent to assert that it exists, rather than just loading all
  tasks with the given parent ID.

  `parent_id` being None is a special case for top-level tasks.
  """
  if parent_id is None:
    return list(token.user.tasks.filter_by(parent_id=None).all())

  (parent,) = auth.load_owned_objects(models.Task, token, 'get tasks', parent_id)

  return parent.children.all() or []


@api.endpoint('/get_task')
def get_task(
    token: 'auth.JWT',
    task_id: 'typevars.ObjectID'
    ) -> 'List[models.Task]':
  """Load a single task."""
  return auth.load_owned_objects(models.Task, token, 'get task', task_id)


@api.endpoint('/add_task')
def add_task(
    token: 'auth.JWT',
    title: str,
    parent_id: 'Optional[typevars.ObjectID]' = None
    ) -> 'List[models.Task]':
  """Add a task with the given title and parent."""
  mutated = auth.load_owned_objects(models.Task, token, 'get tasks', parent_id)

  try:
    before = models.Task.get_by(
        owner=token.user, parent_id=parent_id, after=None)

    mutated.append(before)
  except db_errors.ObjectNotFoundError:
    before = None

  task = models.Task(
      owner=token.user, title=title, parent_id=parent_id, before=before)

  db.DB.session.add(task)
  db.DB.session.commit()

  mutated.append(task)

  return [m for m in set(mutated) if m is not None]


@api.endpoint('/delete_task')
def delete_task(
    token: 'auth.JWT',
    task_id: 'typevars.ObjectID',
    cascade: bool = False
    ) -> 'List[models.Task]':
  """Delete a task.

  If `cascade` is true, then all descendants of the given task are also deleted.
  Otherwise, any child tasks are made children of the deleted task's parent, and
  inserted in the position of the deleted task.
  """
  (task,) = auth.load_owned_objects(models.Task, token, 'get tasks', task_id)

  mutated = [task.parent, task.before, task.after]

  if cascade:
    if task.before is not None:
      task.before.after = task.after
    elif task.after is not None:
      task.after.before = None
  else:
    for child in task.children:
      child.parent = task.parent

      if child.before is None:
        child.before = task.before

      if child.after is None:
        child.after = task.after

      mutated.append(child)

  db.DB.session.delete(task)
  db.DB.session.commit()

  return [m for m in set(mutated) if m is not None]


@api.endpoint('/update_task')
def update_task(
    token: 'auth.JWT',
    task_id: 'typevars.ObjectID',
    **kwargs: 'Any'
    ) -> 'List[models.Task]':
  """Set arbitrary fields on a task."""
  (task,) = auth.load_owned_objects(models.Task, token, 'get tasks', task_id)

  for key, value in kwargs.items():
    try:
      setattr(task, key, value)
    except AttributeError:
      raise util_errors.APIError(
          'Could not set attribute {}'.format(key), 400)

  db.DB.session.commit()

  return [task]


@api.endpoint('/reorder_task')
def reorder_task(
    token: 'auth.JWT',
    task_id: 'typevars.ObjectID',
    before_id: 'Optional[typevars.ObjectID]' = None,
    after_id: 'Optional[typevars.ObjectID]' = None
    ) -> 'List[models.Task]':
  """Change the position of the task in the list."""
  if before_id is None and after_id is None:
    raise util_errors.APIError(
        'One of before_id or after_id must be provided', 400)

  if task_id == before_id or task_id == after_id:
    raise util_errors.APIError(
        'Task cannot be before or after itself', 400)

  before = None
  after = None

  (task, before, after) = auth.load_owned_objects(
      models.Task, token, 'get tasks', task_id, before_id, after_id)

  if before is None:
    before = after.before

  if after is None:
    after = before.after

  if (
      (before is not None and before.after is not after) or
      (after is not None and after.before is not before)):
    raise util_errors.APIError(
        'Before and after tasks are not adjacent', 400)

  mutated = [before, after, task, task.before, task.after]

  if before is not None and task.parent is not before.parent:
    mutated.extend([task.parent, before.parent])
    check_reparent(task, before.parent)
  elif after is not None and task.parent is not after.parent:
    mutated.extend([task.parent, after.parent])
    check_reparent(task, after.parent)

  if task.before is not None:
    task.before.after = task.after
  elif task.after is not None:
    task.after.before = None

  task.before = before
  task.after = after

  db.DB.session.commit()

  return [m for m in set(mutated) if m is not None]


@api.endpoint('/reparent_task')
def reparent_task(
    token: 'auth.JWT',
    task_id: 'typevars.ObjectID',
    parent_id: 'typevars.ObjectID'
    ) -> 'List[models.Task]':
  """Change the parent of a task."""
  (task, parent) = auth.load_owned_objects(
      models.Task, token, 'reparent task', task_id, parent_id)

  mutated = [parent, task, task.parent, task.before, task.after]

  if parent.has_children:
    raise util_errors.APIError(
        'Parent already has children. Use /reorder_task instead', 400)

  check_reparent(task, parent)

  if task.before is not None:
    task.before.after = task.after
  elif task.after is not None:
    task.after.before = None

  task.before = None
  task.after = None

  db.DB.session.commit()

  return [m for m in set(mutated) if m is not None]
