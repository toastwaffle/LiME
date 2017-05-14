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


@api.endpoint('/add_task')
def add_task(token, title, parent_id=None):
  task = models.Task(owner=token.user, title=title, parent_id=parent_id)

  db.DB.session.add(task)
  db.DB.session.commit()

  return task


@api.endpoint('/delete_task')
def delete_task(token, task_id):
  try:
    task = models.Task.get_by(object_id=task_id)
  except db_errors.ObjectNotFoundError:
    raise util_errors.APIError('Could not delete task; task not found', 410)

  if task.owner_id != token.user_id:
    raise util_errors.APIError('Could not delete task; not authorized', 403)

  db.DB.session.delete(task)
  db.DB.session.commit()

  return {}


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

  return task
