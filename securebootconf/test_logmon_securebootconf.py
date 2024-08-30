import unittest
from unittest.mock import mock_open, patch


class TestLogmonSecureBootConf(unittest.TestCase):
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="prop1=value1\nprop2=value2\n",
    )
    def test_secure_boot_config_update(self, mock_file):
        # Mocking the fluentd_config object and updated_value dictionary
        fluentd_config = type("obj", (object,), {"secure_boot_config": "dummy_path"})
        updated_value = {"prop1": "new_value1"}
        props_tup = ("prop1", "prop2")

        # Mocking the file_content list
        file_content = []

        # The code snippet to be tested
        f = open(fluentd_config.secure_boot_config, "r+")
        for line in f.readlines():
            name, var = line.partition("=")[::2]
            if line.startswith(props_tup):
                content = name + "=" + updated_value[name] + "\n"
                file_content.append(content)
            else:
                file_content.append(line)
        f.seek(0)

        # Verify the file content
        expected_content = ["prop1=new_value1\n", "prop2=value2\n"]
        self.assertEqual(file_content, expected_content)

        # Ensure the file was opened correctly
        mock_file.assert_called_once_with("dummy_path", "r+")


if __name__ == "__main__":
    unittest.main()
