"""Views for handling tasks."""

from ..database import db
from ..database import errors as db_errors
from ..database import models
from ..util import api
from ..util import errors as util_errors


def check_owner(token, action, *tasks):
  for task in tasks:
    if task is None:
      continue

    if task.owner_id != token.user_id:
      raise util_errors.APIError(
          'Could not {}; not authorized'.format(action), 403)


def load_tasks(token, action, *task_ids):
  tasks = []

  for task_id in task_ids:
    if task_id is None:
      tasks.append(None)
      continue

    try:
      tasks.append(models.Task.get_by(object_id=task_id))
    except db_errors.ObjectNotFoundError:
      raise util_errors.APIError(
          'Could not {0}; task {1} not found'.format(action, task_id), 410)

  check_owner(token, action, *tasks)

  return tasks


@api.endpoint('/get_tasks')
def get_tasks(token, parent_id=None):
  if parent_id is None:
    return list(token.user.tasks.filter_by(parent_id=None).all())

  (parent,) = load_tasks(token, 'get tasks', parent_id)

  return parent.children.all() or []


@api.endpoint('/get_task')
def get_task(token, task_id):
  return load_tasks(token, 'get task', task_id)


@api.endpoint('/add_task')
def add_task(token, title, parent_id=None):
  mutated = load_tasks(token, 'get tasks', parent_id)

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
def delete_task(token, task_id, cascade=False):
  (task,) = load_tasks(token, 'get tasks', task_id)

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


@api.endpoint('/set_completed_state')
def set_completed_state(token, task_id, completed):
  (task,) = load_tasks(token, 'get tasks', task_id)

  task.completed = completed

  db.DB.session.commit()

  return [task]


@api.endpoint('/reorder_task')
def reorder_task(token, task_id, before_id=None, after_id=None):
  if before_id is None and after_id is None:
    raise util_errors.APIError(
        'One of before_id or after_id must be provided', 400)

  if task_id == before_id or task_id == after_id:
    raise util_errors.APIError(
        'Task cannot be before or after itself', 400)

  before = None
  after = None

  (task, before, after) = load_tasks(
      token, 'get tasks', task_id, before_id, after_id)

  if before is None:
    before = after.before

  if after is None:
    after = before.after

  if (
      before is not None and before.after is not after) or (
      after is not None and after.before is not before):
    raise util_errors.APIError(
        'Before and after tasks are not adjacent', 400)

  mutated = [before, after, task, task.before, task.after]

  if before is not None and task.parent is not before.parent:
    mutated.extend([task.parent, before.parent])
    task.parent = before.parent
  elif after is not None and task.parent is not after.parent:
    mutated.extend([task.parent, after.parent])
    task.parent = after.parent

  if task.before is not None:
    task.before.after = task.after
  elif task.after is not None:
    task.after.before = None

  task.before = before
  task.after = after

  db.DB.session.commit()

  return [m for m in set(mutated) if m is not None]
