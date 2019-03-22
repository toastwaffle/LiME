"""Tests for the password descriptor.

Relies on the descriptor existing on the user model.
"""

from absl.testing import absltest
from passlib import context

from lime import app
from lime.database import models
from lime.util import testing


class PasswordsTest(absltest.TestCase):
  """Tests for the password descriptor."""

  def test_check(self):
    """A password can be checked against a known hash."""
    with testing.test_setup():
      user = models.User(password_hash=(
          '$2b$12$3a9NGwLSNf/B0s4QPTvTgeC0JKA7Qf.IbU7WDIb7l9hGbi3DShnCO'))

      self.assertFalse(user.password == 'qwertyuiop')
      self.assertTrue(user.password == 'password')

  def test_set_and_check(self):
    """A password can be set and checked against."""
    with testing.test_setup():
      user = models.User()

      self.assertEqual(user.password_hash, None)

      user.password = 'password'

      self.assertNotEmpty(user.password_hash)
      self.assertTrue(user.password == 'password')

  def test_update(self):
    """The password hash is updated when it uses an old hash algorithm."""
    with testing.test_setup():
      app.APP.config['PASSLIB_CONTEXT'] = context.CryptContext(
          schemes=['bcrypt', 'md5_crypt'], deprecated='auto')

      md5_hash = '$1$7BYN8u/S$OQOqfmrz8B6vSJn0nApt/.'
      user = models.User(password_hash=md5_hash)

      self.assertTrue(user.password == 'password')
      self.assertNotEqual(user.password_hash, md5_hash)


if __name__ == '__main__':
  absltest.main()
