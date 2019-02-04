"""Tests for Setting model."""

from absl.testing import absltest
from absl.testing import parameterized

from lime.database import setting
from lime.database import user  # required to initialize SQLAlchemy mapper. pylint: disable=unused-import


class SettingTest(parameterized.TestCase):
  """Tests for Setting model."""

  @parameterized.parameters(
      (setting.SettingType.INT, 123),
      (setting.SettingType.FLOAT, 1.23),
      (setting.SettingType.STRING, '123'),
      (setting.SettingType.BOOL, True))
  def test_value(self, setting_type, value):
    """Test value property and setter."""
    s = setting.Setting(setting_type=setting_type)

    self.assertEqual(None, s.value)

    s.value = value

    self.assertEqual(value, s.value)


if __name__ == '__main__':
  absltest.main()
