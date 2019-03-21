"""Tests for authentication library."""

import datetime
import time

from absl.testing import absltest

from lime import app
from lime.database import db
from lime.database import models
from lime.util import auth
from lime.util import errors
from lime.util import testing

# pylint: disable=no-self-use


class AuthTest(absltest.TestCase):
  """Tests for authentication library."""

  def test_check_valid__valid(self):  # pylint: disable=no-self-use
    """A token built from a user is valid."""
    with testing.test_setup():
      # Would raise an exception if invalid
      auth.JWT.from_user(models.User(object_id=1)).check_valid()

  def test_check_valid__invalid(self):
    """An invalid token makes check_valid raise an exception."""
    with testing.test_setup():
      with self.assertRaises(errors.AuthenticationError):
        auth.JWT(1, 'foo').check_valid()

  def test_check_valid__expires(self):
    """A token expires after the expiry time."""
    with testing.test_setup():
      app.APP.config['JWT_EXPIRY'] = datetime.timedelta(seconds=1)

      token = auth.JWT.from_user(models.User(object_id=1))
      # Would raise an exception if invalid
      token.check_valid()

      time.sleep(2)

      with self.assertRaises(errors.AuthenticationError):
        token.check_valid()

  def test_user(self):
    """A token expires after the expiry time."""
    with testing.test_setup():
      user = models.User(name='test', email='test@test.com', password='test')
      db.DB.session.add(user)
      db.DB.session.commit()

      token = auth.JWT.from_user(user)

      self.assertEqual(auth.JWT(1, token.key).user, user)

  def test_to_from_json(self):
    """A token serializes and deserializes and is still valid."""
    with testing.test_setup():
      # Would raise an exception if invalid
      auth.JWT.from_json(
          auth.JWT.from_user(models.User(object_id=1)).to_json()
      ).check_valid()

  def test_check_owner__valid(self):
    """Objects owned by the token bearer are accepted."""
    with testing.test_setup():
      user = models.User(name='test', email='test@test.com', password='test')
      task1 = models.Task(title='Foo', owner=user)
      task2 = models.Task(title='Bar', owner=user)
      db.DB.session.add_all([user, task1, task2])
      db.DB.session.commit()

      token = auth.JWT.from_user(user)

      auth.check_owner(token, 'check owner', task1, task2)

  def test_check_owner__not_owned(self):
    """Objects not owned by the token bearer raise an exception."""
    with testing.test_setup():
      user1 = models.User(name='test', email='test@test.com', password='test')
      user2 = models.User(name='test2', email='test2@test.com', password='test')
      task1 = models.Task(title='Foo', owner=user1)
      task2 = models.Task(title='Bar', owner=user2)
      db.DB.session.add_all([user1, user2, task1, task2])
      db.DB.session.commit()

      token = auth.JWT.from_user(user1)

      with self.assertRaises(errors.APIError):
        auth.check_owner(token, 'check owner', task1, task2)

  def test_load_owned_objects__valid(self):
    """Objects owned by the token bearer are loaded."""
    with testing.test_setup():
      user = models.User(name='test', email='test@test.com', password='test')
      task1 = models.Task(title='Foo', owner=user)
      task2 = models.Task(title='Bar', owner=user)
      db.DB.session.add_all([user, task1, task2])
      db.DB.session.commit()

      token = auth.JWT.from_user(user)

      objects = auth.load_owned_objects(
          models.Task, token, 'load owned objects', None, 1, 2)

      self.assertEqual(objects[0], None)
      self.assertEqual(objects[1], task1)
      self.assertEqual(objects[2], task2)

  def test_load_owned_objects__not_owned(self):
    """Objects not owned by the token bearer raise an exception."""
    with testing.test_setup():
      user1 = models.User(name='test', email='test@test.com', password='test')
      user2 = models.User(name='test2', email='test2@test.com', password='test')
      task1 = models.Task(title='Foo', owner=user1)
      task2 = models.Task(title='Bar', owner=user2)
      db.DB.session.add_all([user1, user2, task1, task2])
      db.DB.session.commit()

      token = auth.JWT.from_user(user1)

      with self.assertRaises(errors.APIError):
        auth.load_owned_objects(
            models.Task, token, 'load owned objects', 1, 2)

  def test_load_owned_objects__non_existent(self):
    """Objects which don't exist raise an exception."""
    with testing.test_setup():
      with self.assertRaises(errors.APIError):
        auth.load_owned_objects(
            models.Task,
            auth.JWT.from_user(models.User(object_id=1)),
            'load owned objects',
            1)

if __name__ == '__main__':
  absltest.main()
