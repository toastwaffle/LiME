"""Tests for Task model."""

from unittest import mock

from absl.testing import absltest

from lime.database import models


class TaskTest(absltest.TestCase):
  """Tests for Task model."""

  def test_before_id(self):
    """Test Task.before_id property when task has a before task."""
    before = models.Task(object_id=1)
    task = models.Task(before=before)

    self.assertEqual(1, task.before_id)

  def test_before_id__no_before(self):
    """Test Task.before_id property when task has no before task."""
    task = models.Task()

    self.assertEqual(None, task.before_id)

  def test_after_id(self):
    """Test Task.after_id property when task has a after task."""
    after = models.Task(object_id=1)
    task = models.Task(after=after)

    self.assertEqual(1, task.after_id)

  def test_after_id__no_after(self):
    """Test Task.after_id property when task has no after task."""
    task = models.Task()

    self.assertEqual(None, task.after_id)

  def test_tag_ids(self):
    """Test Task.tag_ids property."""
    task = models.Task(tags=[
        models.Tag(object_id=1),
        models.Tag(object_id=2),
        models.Tag(object_id=3),
    ])

    self.assertCountEqual([1, 2, 3], task.tag_ids)

  def test_to_json(self):
    """Test Task.to_json()."""

    with mock.patch.object(
        models.Task, 'has_children', new_callable=mock.PropertyMock
    ) as has_children_mock:
      task = models.Task(
          object_id=1,
          title='Task',
          completed=True,
          notes='Notes',
          owner_id=2,
          parent_id=3,
          before=models.Task(object_id=4),
          after=models.Task(object_id=5),
          tags=[
              models.Tag(object_id=1),
              models.Tag(object_id=2),
              models.Tag(object_id=3),
          ])

      has_children_mock.return_value = True

      expected = {
          'object_id': 1,
          'title': 'Task',
          'completed': True,
          'notes': 'Notes',
          'owner_id': 2,
          'parent_id': 3,
          'has_children': True,
          'before_id': 4,
          'after_id': 5,
          'tag_ids': [1, 2, 3],
      }

      self.assertEqual(expected, task.to_json())

      has_children_mock.assert_called_once_with()


if __name__ == '__main__':
  absltest.main()
