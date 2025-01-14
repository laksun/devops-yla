To write unit tests that cover all success and failure cases for the `get_vpce` function, we can use the `unittest` module and mock dependencies like `param_store` and `vpce_exists`. Here's a comprehensive test suite:

---

### Mock Tests for `get_vpce`

```python
import unittest
from unittest.mock import patch, MagicMock


class TestGetVpce(unittest.TestCase):
    @patch("module_name.vpce_exists")
    def test_get_vpce_success(self, mock_vpce_exists):
        from module_name import get_vpce

        # Mock the `param_store` dictionary
        param_store = {
            "/core/logging/vpc-endpoint-vpce-dnsentries": "value:vpce-1234",
            "aws_region": "us-east-1",
            "use_proxy": False,
        }

        # Mock `vpce_exists` to return True
        mock_vpce_exists.return_value = True

        # Call the function
        result = get_vpce("vpc-endpoint", param_store)

        # Assertions
        self.assertEqual(result, "https://vpce-1234")
        mock_vpce_exists.assert_called_once_with("vpce-1234", "us-east-1", False)

    @patch("module_name.vpce_exists")
    def test_get_vpce_missing_param_store_key(self, mock_vpce_exists):
        from module_name import get_vpce

        # Mock the `param_store` dictionary without the required key
        param_store = {
            "aws_region": "us-east-1",
            "use_proxy": False,
        }

        # Call the function
        result = get_vpce("vpc-endpoint", param_store)

        # Assertions
        self.assertEqual(result, "")
        mock_vpce_exists.assert_not_called()

    @patch("module_name.vpce_exists")
    def test_get_vpce_dns_entry_format_error(self, mock_vpce_exists):
        from module_name import get_vpce

        # Mock the `param_store` with an invalid DNS entry format
        param_store = {
            "/core/logging/vpc-endpoint-vpce-dnsentries": "invalid_format",
            "aws_region": "us-east-1",
            "use_proxy": False,
        }

        # Call the function
        result = get_vpce("vpc-endpoint", param_store)

        # Assertions
        self.assertEqual(result, "")
        mock_vpce_exists.assert_not_called()

    @patch("module_name.vpce_exists")
    def test_get_vpce_vpce_does_not_exist(self, mock_vpce_exists):
        from module_name import get_vpce

        # Mock the `param_store` dictionary
        param_store = {
            "/core/logging/vpc-endpoint-vpce-dnsentries": "value:vpce-1234",
            "aws_region": "us-east-1",
            "use_proxy": False,
        }

        # Mock `vpce_exists` to return False
        mock_vpce_exists.return_value = False

        # Call the function
        result = get_vpce("vpc-endpoint", param_store)

        # Assertions
        self.assertEqual(result, "")
        mock_vpce_exists.assert_called_once_with("vpce-1234", "us-east-1", False)

    @patch("module_name.vpce_exists")
    def test_get_vpce_unexpected_exception(self, mock_vpce_exists):
        from module_name import get_vpce

        # Mock the `param_store` dictionary
        param_store = {
            "/core/logging/vpc-endpoint-vpce-dnsentries": "value:vpce-1234",
            "aws_region": "us-east-1",
            "use_proxy": False,
        }

        # Mock `vpce_exists` to raise an exception
        mock_vpce_exists.side_effect = Exception("Unexpected error")

        # Call the function
        result = get_vpce("vpc-endpoint", param_store)

        # Assertions
        self.assertEqual(result, "")
        mock_vpce_exists.assert_called_once_with("vpce-1234", "us-east-1", False)


if __name__ == "__main__":
    unittest.main()
```

---

### Test Cases Breakdown:

1. **`test_get_vpce_success`**:
   - Simulates a successful scenario where the VPC endpoint exists, and the `vpce_exists` function returns `True`.
   - Asserts the correct result and ensures `vpce_exists` is called with the expected arguments.

2. **`test_get_vpce_missing_param_store_key`**:
   - Tests the case where the required parameter is missing from the `param_store`.
   - Asserts that the function returns an empty string (`""`) and that `vpce_exists` is not called.

3. **`test_get_vpce_dns_entry_format_error`**:
   - Tests the case where the DNS entry format in `param_store` is invalid and cannot be parsed.
   - Asserts that the function returns an empty string (`""`) and skips calling `vpce_exists`.

4. **`test_get_vpce_vpce_does_not_exist`**:
   - Tests the case where the VPC endpoint does not exist (i.e., `vpce_exists` returns `False`).
   - Asserts that the function returns an empty string (`""`) and that `vpce_exists` is called.

5. **`test_get_vpce_unexpected_exception`**:
   - Tests the case where an unexpected exception is raised in `vpce_exists`.
   - Asserts that the function logs the error and returns an empty string (`""`).

---

### Mocking Dependencies:
- `param_store`: Simulated as a dictionary for testing purposes.
- `vpce_exists`: Mocked using `unittest.mock.patch` to simulate different scenarios like success, failure, or exceptions.

### Notes:
- Replace `module_name` with the actual module name where the `get_vpce` function is defined.
- Ensure logging is configured in the test environment to capture log outputs for debugging.

This test suite covers all success and failure cases comprehensively.


### add exception

import unittest
from unittest.mock import patch


class TestGetVpce(unittest.TestCase):
    @patch("module_name.vpce_exists")
    @patch("module_name.logging")
    def test_get_vpce_unexpected_exception(self, mock_logging, mock_vpce_exists):
        from module_name import get_vpce

        # Mock the `param_store` dictionary
        param_store = {
            "/core/logging/vpc-endpoint-vpce-dnsentries": "value:vpce-1234",
            "aws_region": "us-east-1",
            "use_proxy": False,
        }

        # Mock `vpce_exists` to raise an exception
        mock_vpce_exists.side_effect = Exception("Unexpected error")

        # Call the function
        result = get_vpce("vpc-endpoint", param_store)

        # Assertions
        self.assertEqual(result, "")  # Expect empty string as return value
        mock_vpce_exists.assert_called_once_with("vpce-1234", "us-east-1", False)

        # Verify logging behavior
        mock_logging.exception.assert_called_once_with("Error encountered in the function get_vpce")
        mock_logging.info.assert_any_call(
            "Invalid value for SSM Parameter /core/logging/vpc-endpoint-vpce-dnsentries: value:vpce-1234"
        )


if __name__ == "__main__":
    unittest.main()



### case for vpce_exist is not called

@patch("module_name.vpce_exists")
    @patch("module_name.logging")
    def test_get_vpce_missing_vpce_param(self, mock_logging, mock_vpce_exists):
        from module_name import get_vpce

        # Mock the `param_store` dictionary without the required vpce_param key
        param_store = {
            "aws_region": "us-east-1",
            "use_proxy": False,
        }

        # Call the function
        result = get_vpce("vpc-endpoint", param_store)

        # Assertions
        self.assertEqual(result, "")  # Expect empty string as return value
        mock_vpce_exists.assert_not_called()  # Ensure vpce_exists is not called
        mock_logging.info.assert_any_call("/core/logging/vpc-endpoint-vpce-dnsentries does not exist in Parameter store")
