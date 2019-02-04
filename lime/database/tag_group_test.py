"""Tests for TagGroup model."""

from absl.testing import absltest

from lime.database import models


class TagGroupTest(absltest.TestCase):
  """Tests for TagGroup model."""

  def test_tag_ids(self):
    """Test TagGroup.tag_ids property."""
    group = models.TagGroup(tags=[
        models.Tag(object_id=1),
        models.Tag(object_id=2),
        models.Tag(object_id=3),
    ])

    self.assertItemsEqual([1, 2, 3], group.tag_ids)

  def test_to_json(self):
    """Test TagGroup.to_json()."""
    group = models.TagGroup(
        object_id=1,
        title="TagGroup",
        owner_id=2,
        tags=[
            models.Tag(object_id=1),
            models.Tag(object_id=2),
            models.Tag(object_id=3),
        ])

    expected = {
        'object_id': 1,
        'title': 'TagGroup',
        'owner_id': 2,
        'tag_ids': [1, 2, 3],
    }

    self.assertCountEqual(expected, group.to_json())


if __name__ == '__main__':
  absltest.main()
