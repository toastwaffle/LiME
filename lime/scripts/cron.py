"""Worker to run repeated tasks on a schedule."""

import contextlib
import datetime
import os
import sys

import flask_script

from lime import app

APP = app.APP

@contextlib.contextmanager
def file_lock(lock_file):
  """Use a lock file to prevent multiple instances of the worker running."""
  if os.path.exists(lock_file):
    print(
      (
        'Only one script can run at once. '
        'Script is locked with {}'
      ).format(lock_file)
    )
    sys.exit(-1)
  else:
    open(lock_file, 'w').write('1')
    try:
      yield
    finally:
      os.remove(lock_file)

def get_last_run_time(timestamp_file):
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

def set_timestamp(timestamp_file, now):
  """Write the time of the current run to the timestamp file.

  Args:
    timestamp_file: (str) absolute path to file containing the timestamp
    now: (datetime.datetime) time at which the script was started
  """
  with open(timestamp_file, 'w') as file_handle:
    file_handle.write(now.strftime('%s'))

def run_5_minutely(now):
  """Run tasks which need to be run every 5 minutes.

  Args:
    now: (datetime.datetime) time at which the script was started
  """
  timestamp_file = os.path.abspath(
    './{}_cron_timestamp_5min.txt'.format(APP.config['ENVIRONMENT'])
  )

  if now - get_last_run_time(timestamp_file) < datetime.timedelta(minutes=5):
    return

  return

def run_20_minutely(now):
  """Run tasks which need to be run every 20 minutes.

  Args:
    now: (datetime.datetime) time at which the script was started
  """
  timestamp_file = os.path.abspath(
    './{}_cron_timestamp_20min.txt'.format(APP.config['ENVIRONMENT'])
  )

  difference = now - get_last_run_time(timestamp_file)

  if difference < datetime.timedelta(minutes=20):
    return

  return

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

      run_5_minutely(now)

      run_20_minutely(now)
