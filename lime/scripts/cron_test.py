"""Tests for the cron scripts."""

import datetime
import os
import tempfile

from absl.testing import absltest

from lime import app
from lime.scripts import cron


DUMMY_DATETIME = datetime.datetime(2009, 2, 13, 23, 31, 30)
DUMMY_TIMESTAMP = '1234567890'


class CronTest(absltest.TestCase):
  """Tests for Cron script helpers."""

  def test_get_timestamp(self):
    """Test get_timestamp."""
    with tempfile.TemporaryDirectory() as tempdir:
      timestamp_file = os.path.join(tempdir, 'timestamp_file')
      with open(timestamp_file, 'w') as fh:
        fh.write(DUMMY_TIMESTAMP)

      self.assertEqual(DUMMY_DATETIME, cron.get_timestamp(timestamp_file))

  def test_get_timestamp__no_timestamp_file(self):
    """Test get_timestamp."""
    with tempfile.TemporaryDirectory() as tempdir:
      timestamp_file = os.path.join(tempdir, 'timestamp_file')

      expected = datetime.datetime(1970, 1, 1, 0, 0)

      self.assertEqual(expected, cron.get_timestamp(timestamp_file))

  def test_set_timestamp(self):
    """Test set_timestamp."""
    with tempfile.TemporaryDirectory() as tempdir:
      timestamp_file = os.path.join(tempdir, 'timestamp_file')

      cron.set_timestamp(timestamp_file, DUMMY_DATETIME)

      with open(timestamp_file) as fh:
        self.assertEqual(DUMMY_TIMESTAMP, fh.read().strip())

  def test_is_due__no_timestamp_file(self):
    """Test is_due with no timestamp file."""
    with tempfile.TemporaryDirectory() as tempdir:
      timestamp_file = os.path.join(tempdir, 'timestamp_file')

      now = DUMMY_DATETIME + datetime.timedelta(minutes=6)

      self.assertTrue(cron.is_due(
          timestamp_file, datetime.timedelta(minutes=5), now))

      self.assertEqual(now, cron.get_timestamp(timestamp_file))

  def test_is_due__is_due(self):
    """Test is_due when due."""
    with tempfile.TemporaryDirectory() as tempdir:
      timestamp_file = os.path.join(tempdir, 'timestamp_file')
      with open(timestamp_file, 'w') as fh:
        fh.write(DUMMY_TIMESTAMP)

      now = DUMMY_DATETIME + datetime.timedelta(minutes=6)

      self.assertTrue(cron.is_due(
          timestamp_file, datetime.timedelta(minutes=5), now))

      self.assertEqual(now, cron.get_timestamp(timestamp_file))

  def test_is_due__not_due(self):
    """Test is_due when not due."""
    with tempfile.TemporaryDirectory() as tempdir:
      timestamp_file = os.path.join(tempdir, 'timestamp_file')
      with open(timestamp_file, 'w') as fh:
        fh.write(DUMMY_TIMESTAMP)

      now = DUMMY_DATETIME + datetime.timedelta(minutes=4)

      self.assertFalse(cron.is_due(
          timestamp_file, datetime.timedelta(minutes=5), now))

      self.assertEqual(DUMMY_DATETIME, cron.get_timestamp(timestamp_file))

  def test_make_timestamp_file(self):
    """Test make_timestamp_file."""
    app.APP.config['ENVIRONMENT'] = 'testing'
    expected = os.path.join(os.getcwd(), 'testing_cron_timestamp_300')
    self.assertEqual(expected,
                     cron.make_timestamp_file(datetime.timedelta(minutes=5)))

if __name__ == '__main__':
  absltest.main()
