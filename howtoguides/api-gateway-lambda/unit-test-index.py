import unittest
from unittest.mock import patch, Mock

# Import the actual handler module
from src.aces_aws.lambdas.role_configuration_api import index


class TestHandlerRoutes(unittest.TestCase):

    @patch(
        "src.aces_aws.lambdas.role_configuration_api.index.get_role_configurations",
        new_callable=Mock,
    )
    def test_get_role_configurations(self, mock_func):
        event = {"httpMethod": "GET", "resource": "/role_configurations"}
        index.routes[("GET", "/role_configurations")] = mock_func

        index.handler(event, {})
        mock_func.assert_called_once_with(event)

    @patch(
        "src.aces_aws.lambdas.role_configuration_api.index.get_module_mappings",
        new_callable=Mock,
    )
    def test_get_module_mappings(self, mock_func):
        event = {"httpMethod": "GET", "resource": "/module-mappings"}
        index.routes[("GET", "/module-mappings")] = mock_func

        index.handler(event, {})
        mock_func.assert_called_once_with(event)

    @patch(
        "src.aces_aws.lambdas.role_configuration_api.index.get_role_configuration_entitlements",
        new_callable=Mock,
    )
    def test_get_role_configuration_entitlements(self, mock_func):
        event = {
            "httpMethod": "GET",
            "resource": "/role_configuration/{roleId}/entitlements",
        }
        index.routes[("GET", "/role_configuration/{roleId}/entitlements")] = mock_func

        index.handler(event, {})
        mock_func.assert_called_once_with(event)

    @patch(
        "src.aces_aws.lambdas.role_configuration_api.index.post_role_configuration",
        new_callable=Mock,
    )
    def test_post_role_configuration(self, mock_func):
        event = {"httpMethod": "POST", "resource": "/role_configuration"}
        index.routes[("POST", "/role_configuration")] = mock_func

        index.handler(event, {})
        mock_func.assert_called_once_with(event)

    @patch(
        "src.aces_aws.lambdas.role_configuration_api.index.post_module_mapping",
        new_callable=Mock,
    )
    def test_post_module_mapping(self, mock_func):
        event = {"httpMethod": "POST", "resource": "/module-mapping"}
        index.routes[("POST", "/module-mapping")] = mock_func

        index.handler(event, {})
        mock_func.assert_called_once_with(event)

    @patch(
        "src.aces_aws.lambdas.role_configuration_api.index.patch_role_configuration",
        new_callable=Mock,
    )
    def test_patch_role_configuration(self, mock_func):
        event = {"httpMethod": "PATCH", "resource": "/role_configuration/{roleId}"}
        index.routes[("PATCH", "/role_configuration/{roleId}")] = mock_func

        index.handler(event, {})
        mock_func.assert_called_once_with(event)

    @patch(
        "src.aces_aws.lambdas.role_configuration_api.index.patch_module_mapping",
        new_callable=Mock,
    )
    def test_patch_module_mapping(self, mock_func):
        event = {"httpMethod": "PATCH", "resource": "/module-mapping/{module_tag}"}
        index.routes[("PATCH", "/module-mapping/{module_tag}")] = mock_func

        index.handler(event, {})
        mock_func.assert_called_once_with(event)


if __name__ == "__main__":
    unittest.main()
