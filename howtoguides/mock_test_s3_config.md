Certainly! Here are three test methods for the `get_s3_config` function you provided. These tests cover:

1. **Valid Configuration File**: Tests the function when the configuration file exists and contains valid key-value pairs.
2. **File Not Found**: Tests the function when the configuration file does not exist.
3. **Invalid Configuration File**: Tests the function when the configuration file exists but contains invalid lines.

We'll use Python's `unittest` framework along with `unittest.mock` to mock file operations and logging.

```python
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import logging

# Assuming the s3_config_file variable and get_s3_config function are accessible
s3_config_file = "/usr/local/bin/s3ConfigFile-cloudwatch.conf"

def get_s3_config():
    defaults = {}
    try:
        if Path(s3_config_file).is_file():
            with Path(s3_config_file).open("r") as s3_conf_file:
                for line in s3_conf_file:
                    name, var = line.partition("=")[::2]
                    defaults[name.strip()] = var.strip()
        else:
            logging.error(f"File {s3_config_file} not found.")
    except Exception:
        logging.exception(f"Error reading S3 configuration file")
    logging.debug(f"Defaults: {defaults}")
    return defaults

class TestGetS3Config(unittest.TestCase):

    @patch('pathlib.Path.is_file', return_value=True)
    @patch('pathlib.Path.open')
    def test_valid_config_file(self, mock_open_path, mock_is_file):
        """Test when the config file exists and contains valid key-value pairs."""
        # Mock the file content with valid key-value pairs
        file_content = ['key1=value1\n', 'key2=value2\n']
        mock_file = MagicMock()
        mock_file.__enter__.return_value = file_content
        mock_open_path.return_value = mock_file

        expected = {'key1': 'value1', 'key2': 'value2'}
        result = get_s3_config()
        self.assertEqual(result, expected)

    @patch('logging.error')
    @patch('pathlib.Path.is_file', return_value=False)
    def test_file_not_found(self, mock_is_file, mock_logging_error):
        """Test when the config file does not exist."""
        expected = {}
        result = get_s3_config()
        self.assertEqual(result, expected)
        mock_logging_error.assert_called_with(f"File {s3_config_file} not found.")

    @patch('logging.exception')
    @patch('pathlib.Path.open')
    @patch('pathlib.Path.is_file', return_value=True)
    def test_invalid_config_file(self, mock_is_file, mock_open_path, mock_logging_exception):
        """Test when the config file contains invalid lines."""
        # Mock the file content with an invalid line (missing '=')
        file_content = ['invalid_line_without_equal\n', 'key2=value2\n']
        mock_file = MagicMock()
        mock_file.__enter__.return_value = file_content
        mock_open_path.return_value = mock_file

        # Adjust the function to handle exceptions for invalid lines
        result = get_s3_config()
        # Depending on how you want to handle invalid lines, you might expect the valid lines to be parsed
        expected = {'invalid_line_without_equal': '', 'key2': 'value2'}
        self.assertEqual(result, expected)
        # Check if an exception was logged
        mock_logging_exception.assert_called()

if __name__ == '__main__':
    unittest.main()
```

**Explanation:**

- **Imports**: We import `unittest`, `unittest.mock`, `Path`, and `logging` to handle testing, mocking, and logging.
- **Mocking File Operations**:
  - We mock `Path.is_file` to simulate whether the file exists.
  - We mock `Path.open` to simulate reading from the file without actually accessing the filesystem.
- **Test Methods**:
  1. **`test_valid_config_file`**:
     - Mocks a file containing valid key-value pairs.
     - Asserts that the function returns the correct dictionary.
  2. **`test_file_not_found`**:
     - Mocks the absence of the file.
     - Asserts that the function returns an empty dictionary.
     - Checks that an error was logged.
  3. **`test_invalid_config_file`**:
     - Mocks a file containing an invalid line.
     - Asserts how the function handles invalid lines (in this case, it includes the invalid line with an empty value).
     - Checks that an exception was logged.

**Note**: The handling of invalid lines in the `get_s3_config` function depends on your requirements. If you prefer the function to skip invalid lines or raise an exception, you may need to adjust the function and the test accordingly.