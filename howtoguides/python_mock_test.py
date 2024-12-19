# test_my_app.py
import unittest
from unittest.mock import patch, MagicMock
from client2 import MyApp
from aws_token_provider import IdentityAssertion


class TestMyApp(unittest.TestCase):
    def setUp(self):
        # Common setup for all tests
        self.environment = "dev"
        self.domain = "example.com"
        self.sid = "12345"
        self.password = "password"
        self.token = "mocked_token"

    def test_my_access_token_with_provided_token(self):
        """
        Test that my_access_token returns the provided token when self._token is set.
        """
        app = MyApp(
            environment=self.environment,
            domain=self.domain,
            sid=self.sid,
            password=self.password,
            token=self.token,  # Providing token
        )

        # Access the cached_property
        access_token = app.my_access_token

        # Assert that the returned token matches the provided token
        self.assertEqual(access_token, self.token)

    @patch("client2.EndpointManager")
    def test_my_access_token_with_local_url(self, mock_endpoint_manager):
        """
        Test that my_access_token returns an empty string when the URL is local.
        """
        # Configure the EndpointManager.LOCAL to return a local URL
        mock_endpoint_manager.LOCAL = "http://docker"

        app = MyApp(
            environment=self.environment,
            domain=self.domain,
            sid=self.sid,
            password=self.password,
            token=None,  # No token provided
        )

        # Mock self._url to be EndpointManager.LOCAL.value
        app._url = mock_endpoint_manager.LOCAL

        # Access the cached_property
        access_token = app.my_access_token

        # Assert that the access token is an empty string
        self.assertEqual(access_token, "")

    @patch("client2.AWSTokenProvider")
    @patch("client2.AwsIdpSdkConfig")
    @patch("client2.EndpointManager.get_environment_config")
    def test_my_access_token_successful_retrieval(
        self, mock_get_env_config, mock_aws_idp_sdk_config, mock_aws_token_provider
    ):
        """
        Test that my_access_token successfully retrieves and returns the access token
        when no token is provided and URL is not local.
        """
        # Setup the environment configuration
        mock_get_env_config.return_value = {
            "endpoint": "https://api.example.com/token",
            "resource": "resource123",
            "role": "role3",
        }

        # Mock the AwsIdpSdkConfig initialization
        mock_sdk_config_instance = MagicMock()
        mock_aws_idp_sdk_config.return_value = mock_sdk_config_instance

        # Mock the AWSTokenProvider instance and its methods
        mock_token_provider_instance = MagicMock()
        mock_aws_token_provider.return_value = mock_token_provider_instance

        # Mock the identity assertion and access token
        mock_identity_assertion = MagicMock(spec=IdentityAssertion)
        mock_identity_assertion.get_access_token.return_value = "retrieved_access_token"
        mock_token_provider_instance.get_identity_assertion.return_value = (
            mock_identity_assertion
        )

        app = MyApp(
            environment=self.environment,
            domain=self.domain,
            sid=self.sid,
            password=self.password,
            token=None,  # No token provided
        )

        # Ensure self._url is not local
        app._url = "https://non-local-url.com"

        # Access the cached_property
        access_token = app.my_access_token

        # Assertions
        self.assertEqual(access_token, "retrieved_access_token")
        mock_get_env_config.assert_called_with(environment=self.environment)
        mock_aws_idp_sdk_config.assert_called_with(region_name="us-east-1")
        mock_aws_token_provider.assert_called_with(
            mock_sdk_config_instance,
            "https://api.example.com/token",
            "resource123",
            "role3",
        )
        mock_token_provider_instance.get_identity_assertion.assert_called_once()
        mock_identity_assertion.get_access_token.assert_called_once()

    @patch("client2.AWSTokenProvider")
    @patch("client2.AwsIdpSdkConfig")
    @patch("client2.EndpointManager.get_environment_config")
    @patch("client2.logging")
    def test_my_access_token_exception_handling(
        self,
        mock_logging,
        mock_get_env_config,
        mock_aws_idp_sdk_config,
        mock_aws_token_provider,
    ):
        """
        Test that my_access_token handles exceptions gracefully and logs an error.
        """
        # Setup the environment configuration
        mock_get_env_config.return_value = {
            "endpoint": "https://api.example.com/token",
            "resource": "resource123",
            "role": "role3",
        }

        # Mock the AwsIdpSdkConfig initialization
        mock_sdk_config_instance = MagicMock()
        mock_aws_idp_sdk_config.return_value = mock_sdk_config_instance

        # Mock the AWSTokenProvider instance and its methods
        mock_token_provider_instance = MagicMock()
        mock_aws_token_provider.return_value = mock_token_provider_instance

        # Configure get_identity_assertion to raise an exception
        mock_token_provider_instance.get_identity_assertion.side_effect = Exception(
            "Token retrieval failed"
        )

        app = MyApp(
            environment=self.environment,
            domain=self.domain,
            sid=self.sid,
            password=self.password,
            token=None,  # No token provided
        )

        # Ensure self._url is not local
        app._url = "https://non-local-url.com"

        # Access the cached_property
        access_token = app.my_access_token

        # Assertions
        self.assertIsNone(
            access_token
        )  # Since exception occurs, the method returns None
        mock_logging.error.assert_called_with(
            "Token not retrieved - Token retrieval failed"
        )

    @patch("client2.AWSTokenProvider")
    @patch("client2.AwsIdpSdkConfig")
    @patch("client2.EndpointManager.get_environment_config")
    def test_my_access_token_cached_property(
        self, mock_get_env_config, mock_aws_idp_sdk_config, mock_aws_token_provider
    ):
        """
        Test that the @cached_property caches the access token after the first retrieval.
        """
        # Setup the environment configuration
        mock_get_env_config.return_value = {
            "endpoint": "https://api.example.com/token",
            "resource": "resource123",
            "role": "role3",
        }

        # Mock the AwsIdpSdkConfig initialization
        mock_sdk_config_instance = MagicMock()
        mock_aws_idp_sdk_config.return_value = mock_sdk_config_instance

        # Mock the AWSTokenProvider instance and its methods
        mock_token_provider_instance = MagicMock()
        mock_aws_token_provider.return_value = mock_token_provider_instance

        # Mock the identity assertion and access token
        mock_identity_assertion = MagicMock(spec=IdentityAssertion)
        mock_identity_assertion.get_access_token.return_value = "cached_access_token"
        mock_token_provider_instance.get_identity_assertion.return_value = (
            mock_identity_assertion
        )

        app = MyApp(
            environment=self.environment,
            domain=self.domain,
            sid=self.sid,
            password=self.password,
            token=None,  # No token provided
        )

        # Ensure self._url is not local
        app._url = "https://non-local-url.com"

        # Access the cached_property multiple times
        access_token_first = app.my_access_token
        access_token_second = app.my_access_token

        # Assertions
        self.assertEqual(access_token_first, "cached_access_token")
        self.assertEqual(access_token_second, "cached_access_token")
        # Ensure that get_identity_assertion is called only once due to caching
        mock_token_provider_instance.get_identity_assertion.assert_called_once()


if __name__ == "__main__":
    unittest.main()
