"""Tests for cross domain headers library."""

from absl.testing import absltest

from lime import app
from lime.util import crossdomain

class CrossdomainTest(absltest.TestCase):
  """Tests for cross domain headers library."""

  def test_allow(self):
    """The Access-Control headers are set."""
    @app.APP.route('/', methods=['GET', 'OPTIONS'])
    @crossdomain.allow(
        origins=['foo.com', 'bar.net'],
        headers=['Content-Type', 'Accept'])
    def f():  # pylint: disable=unused-variable
      return ""

    with app.APP.test_client() as c:
      resp = c.options('/')

    self.assertEqual(
        resp.headers['Access-Control-Allow-Origin'], 'foo.com, bar.net')
    self.assertEqual(
        resp.headers['Access-Control-Allow-Headers'], 'CONTENT-TYPE, ACCEPT')
    self.assertEqual(
        # Header order is not fixed.
        sorted(resp.headers['Access-Control-Allow-Methods'].split(', ')),
        ['GET', 'HEAD', 'OPTIONS'])
    self.assertEqual(
        resp.headers['Access-Control-Max-Age'], '21600')

if __name__ == '__main__':
  absltest.main()
