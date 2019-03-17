"""Tests for User model."""

from absl.testing import absltest

from lime.database import db
from lime.database import models
from lime.util import settings_enums
from lime.util import testing


class UserTest(absltest.TestCase):
  """Tests for User model."""

  def test_get_setting__setting_exists(self):
    """Test User.get_settings when the setting exists."""
    with testing.test_setup():
      user = models.User(name='test', email='test@test.com', password='test')
      user.deletion_behaviour = settings_enums.DeletionBehaviour.CASCADE
      db.DB.session.add(user)
      db.DB.session.commit()

      setting = user.get_setting('deletion_behaviour')

      self.assertEqual('deletion_behaviour', setting.key)
      self.assertEqual(settings_enums.DeletionBehaviour.CASCADE.value,
                       setting.value)

  def test_get_setting__setting_does_not_exist(self):
    """Test User.get_settings when the setting does not exist."""
    with testing.test_setup():
      user = models.User(name='test', email='test@test.com', password='test')
      db.DB.session.add(user)
      db.DB.session.commit()

      with self.assertRaises(KeyError):
        user.get_setting('does_not_exist')

  def test_to_json(self):
    """Test User.to_json."""
    # Settings mechanism requires interaction with the database
    with testing.test_setup():
      user = models.User(name='test', email='test@test.com', password='test')
      user.deletion_behaviour = settings_enums.DeletionBehaviour.CASCADE
      user.language = settings_enums.Language.EN_GB
      db.DB.session.add(user)
      db.DB.session.commit()

      expected = {
          'object_id': 1,
          'name': 'test',
          'email': 'test@test.com',
          'deletion_behaviour': settings_enums.DeletionBehaviour.CASCADE,
          'language': settings_enums.Language.EN_GB,
      }

      self.assertEqual(expected, user.to_json())


if __name__ == '__main__':
  absltest.main()
