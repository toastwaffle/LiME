"""Tests for API library."""

import enum

from absl.testing import absltest

from lime import app
from lime.system import setup
from lime.util import api
from lime.util import errors
from lime.util import testing

# pylint: disable=no-self-use,unused-variable,missing-docstring,protected-access,blacklisted-name

class APISerializationTest(absltest.TestCase):
  """Tests for API library serialization/deserialization methods."""

  def setUp(self):
    api._SERIALIAZABLE_CLASSES_BY_CLASS = {}
    api._SERIALIAZABLE_CLASSES_BY_IDENTIFIER = {}

  def test_register_serializable__no_to_json(self):
    """Error is raised when registering a class with no to_json()."""
    with self.assertRaises(errors.SerializationError):
      @api.register_serializable()
      class Foo():
        pass

  def test_register_serializable__duplicate_identifier(self):
    """Error is raised when registering 2 classes with the same identifier."""
    with self.assertRaises(errors.SerializationError):
      @api.register_serializable()
      class Foo():
        def to_json(self):
          pass

      @api.register_serializable('Foo')
      class Bar():
        def to_json(self):
          pass

  def test_encoder__enum(self):
    """Encoder encodes an enum to its value."""
    class Foo(enum.Enum):
      FOO = 'foo'

    self.assertEqual(api.ENCODER.encode(Foo.FOO), '"foo"')

  def test_encoder__serializable(self):
    """Encoder encodes an serializable class."""
    @api.register_serializable()
    class Foo():
      def to_json(self):
        return {'foo': 'foo'}

    self.assertEqual(
        api.ENCODER.encode(Foo()),
        '{"foo": "foo", "__identifier": "Foo"}')

  def test_encoder__passthrough(self):
    """Encoder passes through to the default JSON encoder."""
    self.assertEqual(api.ENCODER.encode({}), '{}')

  def test_from_dict__known_class(self):
    """from_dict decodes a known class."""
    @api.register_serializable()
    class Foo():
      def to_json(self):
        pass
      @classmethod
      def from_json(cls, _):
        return 'sentinel'

    self.assertEqual(api.from_dict({'__identifier': 'Foo'}), 'sentinel')

  def test_from_dict__unknown_class(self):
    """from_dict ignored an unknown class."""
    self.assertEqual(
        api.from_dict({'__identifier': 'Foo'}),
        {'__identifier': 'Foo'})

  def test_from_dict__no_identifer(self):
    """from_dict ignored an unknown class."""
    self.assertEqual(api.from_dict({}), {})

class APIEndpointTest(absltest.TestCase):
  """Tests for API library serialization/deserialization methods."""

  def test_bad_request(self):
    """Error 400 when request cannot be deserialized."""
    with app.APP.test_client() as c:
      resp = c.post('/', data='{', content_type='application/json')
      self.assertEqual(resp.status, '400 BAD REQUEST')
      self.assertEqual(resp.get_data(as_text=True), (
          '{"error": "Could not parse request: Expecting property name '
          'enclosed in double quotes: line 1 column 2 (char 1)"}'))

  def test_no_token(self):
    """Error 401 when token is missing."""
    with app.APP.test_client() as c:
      resp = c.post('/', data='{}', content_type='application/json')
      self.assertEqual(resp.status, '401 UNAUTHORIZED')
      self.assertEqual(
          resp.get_data(as_text=True),
          '{"error": "No authentication token provided."}')

  def test_no_token__no_auth_required(self):
    """200 OK when token not required."""
    with app.APP.test_client() as c:
      resp = c.post('/no_auth', data='{}', content_type='application/json')
      self.assertEqual(resp.status, '200 OK')
      self.assertEqual(resp.get_data(as_text=True), '{"bar": "foo"}')

  def test_invalid_token(self):
    """Error 401 when token is invalid."""
    with app.APP.test_client() as c:
      resp = c.post(
          '/',
          data='{"token": {"user_id":1,"key":"","__identifier":"JWT"}}',
          content_type='application/json')
      self.assertEqual(resp.status, '401 UNAUTHORIZED')
      self.assertEqual(
          resp.get_data(as_text=True),
          '{"error": "Authentication token not valid."}')

  def test_unparsed_token(self):
    """Error 401 when token is not parsed to a JWT object."""
    with app.APP.test_client() as c:
      resp = c.post(
          '/',
          data='{"token": {"user_id":1,"key":""}}',
          content_type='application/json')
      self.assertEqual(resp.status, '401 UNAUTHORIZED')
      self.assertEqual(
          resp.get_data(as_text=True),
          '{"error": "Could not parse authentication token."}')

  def test_valid_token(self):
    """200 OK when token valid."""
    with app.APP.test_client() as c:
      resp = c.post(
          '/',
          data=testing.with_token({}),
          content_type='application/json')
      self.assertEqual(resp.status, '200 OK')
      self.assertEqual(resp.get_data(as_text=True), '{"foo": "bar"}')

  def test_options(self):
    """Crossdomain options are included."""
    with app.APP.test_client() as c:
      resp = c.options('/no_auth')
      self.assertEqual(resp.status, '200 OK')
      self.assertEqual(resp.headers['Access-Control-Allow-Origin'], '*')
      self.assertEqual(
          resp.headers['Access-Control-Allow-Headers'],
          'CONTENT-TYPE, ACCEPT')


if __name__ == '__main__':
  setup.load_config('testing')

  @api.endpoint('/')
  def foo(*_, **__):
    return {'foo': 'bar'}

  @api.endpoint('/no_auth', require_auth=False)
  def bar(*_, **__):
    return {'bar': 'foo'}

  app.APP.register_blueprint(api.API)

  absltest.main()
