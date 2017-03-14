"""Views for handling tasks."""

from ..database import db
from ..database import errors as db_errors
from ..database import models
from ..util import api
from ..util import errors as util_errors


@api.endpoint('/get_tasks')
def get_tasks(token):
  return list(token.user.tasks.all())


@api.endpoint('/add_task')
def add_task(token, title):
  task = models.Task(owner=token.user, title=title)

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
