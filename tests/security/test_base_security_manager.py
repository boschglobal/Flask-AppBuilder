import datetime
import json
import unittest
from unittest.mock import MagicMock, patch

from flask_appbuilder.security.manager import BaseSecurityManager
from flask_appbuilder.security.manager import JsonWebKey, jwt

JWTClaimsMock = MagicMock()


@patch.object(BaseSecurityManager, "update_user")
@patch.object(BaseSecurityManager, "__init__", return_value=None)
class BaseSecurityManagerUpdateUserAuthStatTestCase(unittest.TestCase):
    def test_first_successful_auth(self, mock1, mock2):
        bsm = BaseSecurityManager()

        user_mock = MagicMock()
        user_mock.login_count = None
        user_mock.fail_login_count = None
        user_mock.last_login = None

        bsm.update_user_auth_stat(user_mock, success=True)

        self.assertEqual(user_mock.login_count, 1)
        self.assertEqual(user_mock.fail_login_count, 0)
        self.assertEqual(type(user_mock.last_login), datetime.datetime)
        self.assertTrue(bsm.update_user.called_once)

    def test_first_unsuccessful_auth(self, mock1, mock2):
        bsm = BaseSecurityManager()

        user_mock = MagicMock()
        user_mock.login_count = None
        user_mock.fail_login_count = None
        user_mock.last_login = None

        bsm.update_user_auth_stat(user_mock, success=False)

        self.assertEqual(user_mock.login_count, 0)
        self.assertEqual(user_mock.fail_login_count, 1)
        self.assertEqual(user_mock.last_login, None)
        self.assertTrue(bsm.update_user.called_once)

    def test_subsequent_successful_auth(self, mock1, mock2):
        bsm = BaseSecurityManager()

        user_mock = MagicMock()
        user_mock.login_count = 5
        user_mock.fail_login_count = 9
        user_mock.last_login = None

        bsm.update_user_auth_stat(user_mock, success=True)

        self.assertEqual(user_mock.login_count, 6)
        self.assertEqual(user_mock.fail_login_count, 0)
        self.assertEqual(type(user_mock.last_login), datetime.datetime)
        self.assertTrue(bsm.update_user.called_once)

    def test_subsequent_unsuccessful_auth(self, mock1, mock2):
        bsm = BaseSecurityManager()

        user_mock = MagicMock()
        user_mock.login_count = 5
        user_mock.fail_login_count = 9
        user_mock.last_login = None

        bsm.update_user_auth_stat(user_mock, success=False)

        self.assertEqual(user_mock.login_count, 5)
        self.assertEqual(user_mock.fail_login_count, 10)
        self.assertEqual(user_mock.last_login, None)
        self.assertTrue(bsm.update_user.called_once)

    @patch.object(JsonWebKey, "import_key_set", MagicMock())
    @patch.object(jwt, "decode", MagicMock(return_value=JWTClaimsMock))
    @patch.object(json, "dumps", MagicMock(return_value="DecodedExampleAzureJWT"))
    def test_azure_jwt_validated(self, mock1, mock2):
        bsm = BaseSecurityManager()

        bsm._decode_and_validate_azure_jwt("ExampleAzureJWT")
        JWTClaimsMock.validate.assert_called()
