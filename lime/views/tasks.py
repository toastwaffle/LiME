"""Views for handling tasks."""

from ..database import db
from ..database import errors as db_errors
from ..database import models
from ..util import api
from ..util import errors as util_errors


@api.endpoint('/get_tasks')
def get_tasks(token, parent_id=None):
  if parent_id is None:
    return list(token.user.tasks.filter_by(parent_id=None).all())

  try:
    task = models.Task.get_by(object_id=parent_id)
  except db_errors.ObjectNotFoundError:
    raise util_errors.APIError(
        'Could not get tasks; parent task not found', 410)

  if task.owner_id != token.user_id:
    raise util_errors.APIError('Could not get tasks; not authorized', 403)

  return task.children.all() or []


@api.endpoint('/get_task')
def get_task(token, task_id):
  try:
    task = models.Task.get_by(object_id=task_id)
  except db_errors.ObjectNotFoundError:
    raise util_errors.APIError('Could not get task; task not found', 410)

  if task.owner_id != token.user_id:
    raise util_errors.APIError('Could not get task; not authorized', 403)

  return [task]


@api.endpoint('/add_task')
def add_task(token, title, parent_id=None):
  mutated = []

  if parent_id is not None:
    try:
      parent = models.Task.get_by(object_id=parent_id)
    except db_errors.ObjectNotFoundError:
      raise util_errors.APIError(
          'Could not add task; parent task not found', 410)

    if parent.owner_id != token.user_id:
      raise util_errors.APIError('Could not add task; not authorized', 403)

    mutated.append(parent)

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

  return mutated


@api.endpoint('/delete_task')
def delete_task(token, task_id, cascade=False):
  try:
    task = models.Task.get_by(object_id=task_id)
  except db_errors.ObjectNotFoundError:
    raise util_errors.APIError('Could not delete task; task not found', 410)

  if task.owner_id != token.user_id:
    raise util_errors.APIError('Could not delete task; not authorized', 403)

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

  return [m for m in mutated if m is not None]


@api.endpoint('/set_completed_state')
def set_completed_state(token, task_id, completed):
  try:
    task = models.Task.get_by(object_id=task_id)
  except db_errors.ObjectNotFoundError:
    raise util_errors.APIError(
        'Could not set task completed state; task not found', 410)

  if task.owner_id != token.user_id:
    raise util_errors.APIError(
        'Could not set task completed state; not authorized', 403)

  task.completed = completed

  db.DB.session.commit()

  return [task]

@api.endpoint('/reorder_task')
def reorder_task(token, task_id, before_id=None, after_id=None):
  if before_id is None and after_id is None:
    raise util_errors.APIError(
        'One of before_id or after_id must be provided', 400)

  before = None
  after = None

  if before_id is not None:
    try:
      before = models.Task.get_by(object_id=before_id)
    except db_errors.ObjectNotFoundError:
      raise util_errors.APIError(
          'Could not reorder task; before task not found', 410)

  if after_id is not None:
    try:
      after = models.Task.get_by(object_id=after_id)
    except db_errors.ObjectNotFoundError:
      raise util_errors.APIError(
          'Could not reorder task; after task not found', 410)

  if before is None:
    before = after.before

  if after is None:
    after = before.after

  if (
      before is not None and before.after is not after) or (
      after is not None and after.before is not before):
    raise util_errors.APIError(
        'Before and after tasks are not adjacent', 400)

  try:
    task = models.Task.get_by(object_id=task_id)
  except db_errors.ObjectNotFoundError:
    raise util_errors.APIError(
        'Could not reorder task; task not found', 410)

  mutated = [
      m
      for m in set([before, after, task, task.before, task.after])
      if m is not None
  ]

  if task.before is not None:
    task.before.after = task.after
  elif task.after is not None:
    task.after.before = None

  task.before = before
  task.after = after

  db.DB.session.commit()

  return mutated
