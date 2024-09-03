import unittest
from unittest.mock import patch, mock_open, MagicMock
import os

# Assuming replace_fluentd_placeholders is imported from the module where it's defined
# from your_module import replace_fluentd_placeholders


class TestReplaceFluentaPlaceholders(unittest.TestCase):

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="<<ADD_DESTINATION_CONFIG>> <<ADD_REGION>> <<ADD_INSTANCE_ID>>",
    )
    @patch("os.rename")
    @patch("os.remove")
    @patch("your_module.get_vpce", return_value=None)  # Mocking get_vpce function
    @patch(
        "your_module.is_vpce_enabled", return_value=False
    )  # Mocking is_vpce_enabled function
    @patch("your_module.set_file_perms")
    def test_basic_placeholder_replacement(
        self,
        mock_set_perms,
        mock_is_vpce_enabled,
        mock_get_vpce,
        mock_remove,
        mock_rename,
        mock_open,
    ):
        # Prepare the test data
        fluentd_config = MagicMock()
        replace_fluentd_placeholders(
            fluentd_config=fluentd_config,
            file="test_file.conf",
            region="us-west-2",
            instance_id="i-1234567890abcdef",
            http_proxy_port=3128,
            target_s3_bucket=None,
            dest_output_conf="destination_config",
            is_high_memory_instance=False,
            paramstore_config=None,
        )

        # Check that the rename and file operations were performed correctly
        mock_rename.assert_called_once_with("test_file.conf", "test_file.conf-param")
        mock_remove.assert_called_once_with("test_file.conf-param")

        # Check that the file was written with the expected content
        handle = mock_open()
        handle.write.assert_called_once_with(
            "destination_config us-west-2 i-1234567890abcdef"
        )
        mock_set_perms.assert_called_once_with(
            "test_file.conf", fluentd_config.fluentd_user, 0o0640
        )

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="<<ADD_HTTP_PROXY>> <<ADD_HTTP_PROXY_CLOUDWATCH>>",
    )
    @patch("os.rename")
    @patch("os.remove")
    @patch("your_module.get_vpce", return_value="vpce-endpoint")
    @patch("your_module.is_vpce_enabled", return_value=False)
    @patch("your_module.set_file_perms")
    def test_proxy_replacement_with_vpce(
        self,
        mock_set_perms,
        mock_is_vpce_enabled,
        mock_get_vpce,
        mock_remove,
        mock_rename,
        mock_open,
    ):
        fluentd_config = MagicMock()
        replace_fluentd_placeholders(
            fluentd_config=fluentd_config,
            file="test_file.conf",
            region="us-west-2",
            instance_id="i-1234567890abcdef",
            http_proxy_port=3128,
            target_s3_bucket=None,
            dest_output_conf="destination_config",
            is_high_memory_instance=False,
            paramstore_config=None,
        )

        handle = mock_open()
        handle.write.assert_called_once_with(
            "endpoint vpce-endpoint endpoint vpce-endpoint"
        )

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="<<ADD_BUFFER_SIZE>> <<ADD_FLUSH_THREAD_COUNT>>",
    )
    @patch("os.rename")
    @patch("os.remove")
    @patch("your_module.get_vpce", return_value=None)
    @patch("your_module.is_vpce_enabled", return_value=False)
    @patch("your_module.set_file_perms")
    def test_high_memory_instance(
        self,
        mock_set_perms,
        mock_is_vpce_enabled,
        mock_get_vpce,
        mock_remove,
        mock_rename,
        mock_open,
    ):
        fluentd_config = MagicMock()
        replace_fluentd_placeholders(
            fluentd_config=fluentd_config,
            file="test_file.conf",
            region="us-west-2",
            instance_id="i-1234567890abcdef",
            http_proxy_port=3128,
            target_s3_bucket=None,
            dest_output_conf="destination_config",
            is_high_memory_instance=True,
            paramstore_config=None,
        )

        handle = mock_open()
        handle.write.assert_called_once_with("1024MB 4")

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="<<S3_APP_BUCKET>> <<ADD_S3_PATH>>",
    )
    @patch("os.rename")
    @patch("os.remove")
    @patch("your_module.get_vpce", return_value=None)
    @patch("your_module.is_vpce_enabled", return_value=False)
    @patch("your_module.set_file_perms")
    def test_s3_bucket_replacement(
        self,
        mock_set_perms,
        mock_is_vpce_enabled,
        mock_get_vpce,
        mock_remove,
        mock_rename,
        mock_open,
    ):
        fluentd_config = MagicMock()
        replace_fluentd_placeholders(
            fluentd_config=fluentd_config,
            file="test_file.conf",
            region="us-west-2",
            instance_id="i-1234567890abcdef",
            http_proxy_port=3128,
            target_s3_bucket="my-s3-bucket",
            dest_output_conf="destination_config",
            is_high_memory_instance=False,
            paramstore_config=None,
        )

        handle = mock_open()
        handle.write.assert_called_once_with("my-s3-bucket applogs codedeploylogs")


if __name__ == "__main__":
    unittest.main()
