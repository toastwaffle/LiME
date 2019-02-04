"""Tests for Tag model."""

from absl.testing import absltest

from lime.database import models


class TagTest(absltest.TestCase):
  """Tests for Tag model."""

  def test_owner__in_group(self):
    """Test Tag.owner property when tag is in a group."""
    user = models.User(object_id=1)
    tag_group = models.TagGroup(object_id=2, owner=user)
    tag = models.Tag(group=tag_group)

    self.assertEqual(user, tag.owner)

  def test_owner__not_in_group(self):
    """Test Tag.owner property when tag is not in a group."""
    user = models.User(object_id=1)
    tag = models.Tag(direct_owner=user)

    self.assertEqual(user, tag.owner)

  def test_before_id(self):
    """Test Tag.before_id property when tag has a before tag."""
    before = models.Tag(object_id=1)
    tag = models.Tag(before=before)

    self.assertEqual(1, tag.before_id)

  def test_before_id__no_before(self):
    """Test Tag.before_id property when tag has no before tag."""
    tag = models.Tag()

    self.assertEqual(None, tag.before_id)

  def test_after_id(self):
    """Test Tag.after_id property when tag has a after tag."""
    after = models.Tag(object_id=1)
    tag = models.Tag(after=after)

    self.assertEqual(1, tag.after_id)

  def test_after_id__no_after(self):
    """Test Tag.after_id property when tag has no after tag."""
    tag = models.Tag()

    self.assertEqual(None, tag.after_id)

  def test_to_json__in_group(self):
    """Test serialization of Tag when not in a group."""
    before = models.Tag(object_id=3)
    after = models.Tag(object_id=4)

    tag = models.Tag(
        object_id=1,
        group_id=2,
        title='Tag',
        before=before,
        after=after)

    expected = {
        'object_id': 1,
        'title': 'Tag',
        'owner_id': None,
        'group_id': 2,
        'before_id': 3,
        'after_id': 4,
    }

    self.assertEqual(expected, tag.to_json())

  def test_to_json__not_in_group(self):
    """Test serialization of Tag when not in a group."""
    before = models.Tag(object_id=3)
    after = models.Tag(object_id=4)

    tag = models.Tag(
        object_id=1,
        owner_id=2,
        title='Tag',
        before=before,
        after=after)

    expected = {
        'object_id': 1,
        'title': 'Tag',
        'owner_id': 2,
        'group_id': None,
        'before_id': 3,
        'after_id': 4,
    }

    self.assertEqual(expected, tag.to_json())


if __name__ == '__main__':
  absltest.main()
