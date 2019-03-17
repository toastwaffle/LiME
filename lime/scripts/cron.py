"""Worker to run repeated tasks on a schedule."""

import collections
import contextlib
import datetime
import os
import sys
import typing

import flask_script

from lime import app

# pylint: disable=unused-import,ungrouped-imports,invalid-name
if typing.TYPE_CHECKING:
  from typing import (
      Callable,
      Generator,
  )
# pylint: enable=unused-import,ungrouped-imports,invalid-name

APP = app.APP


@contextlib.contextmanager
def file_lock(lock_file: str) -> 'Generator[None, None, None]':
  """Use a lock file to prevent multiple instances of the worker running."""
  # TODO: consider writing an sh_test for this.
  if os.path.exists(lock_file):
    print('Only one script can run at once. Script is locked with {}'.format(
        lock_file))
    sys.exit(-1)
  else:
    open(lock_file, 'w').write('1')
    try:
      yield
    finally:
      os.remove(lock_file)


def get_timestamp(timestamp_file: str) -> 'datetime.datetime':
  """Get the time at which the set of tasks was last run.

  Args:
    timestamp_file: (str) absolute path to file containing the timestamp

  Returns:
    (datetime.datetime) The datetime.datetime object representing the time
      in the timestamp
  """
  try:
    with open(timestamp_file, 'r') as file_handle:
      timestamp = int(file_handle.read().strip())
  except IOError:
    print('Timestamp not found')
    timestamp = 0

  return datetime.datetime.fromtimestamp(timestamp)


def set_timestamp(timestamp_file: str, now: 'datetime.datetime') -> None:
  """Write the time of the current run to the timestamp file.

  Args:
    timestamp_file: (str) absolute path to file containing the timestamp
    now: (datetime.datetime) time at which the script was started
  """
  with open(timestamp_file, 'w') as file_handle:
    file_handle.write(now.strftime('%s'))


def is_due(timestamp_file: str, delta: 'datetime.timedelta',
           now: 'datetime.datetime'):
  """Test whether a set of tasks at a given frequency is due to be run."""
  if now - get_timestamp(timestamp_file) < delta:
    return False

  set_timestamp(timestamp_file, now)

  return True


def make_timestamp_file(delta):
  """Generate the path to the timestamp file."""
  return os.path.abspath('./{}_cron_timestamp_{}'.format(
      APP.config['ENVIRONMENT'], delta.seconds))


TASKS: 'Dict[datetime.timedelta, Callable]' = collections.defaultdict(list)


def frequency(**kwargs) -> 'Callable[[Callable], Callable]':
  """Register a task to run at a given frequency."""
  def decorator(func: 'Callable') -> 'Callable':
    TASKS[datetime.timedelta(**kwargs)].append(func)

  return decorator


class CronCommand(flask_script.Command):
  """Flask Script command for running Cron jobs."""

  help = 'Run cron jobs'

  @staticmethod
  def run(): # false positive pylint: disable=method-hidden
    """Check the lock, do some setup and run the tasks."""
    with file_lock(
        os.path.abspath('./{}.cron.lock'.format(APP.config['ENVIRONMENT']))
    ):
      now = datetime.datetime.utcnow()

      for delta, tasks in TASKS.items():
        if is_due(make_timestamp_file(delta), delta, now):
          for task in tasks:
            task()
