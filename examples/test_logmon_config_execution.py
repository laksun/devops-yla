import unittest
from unittest.mock import patch
import os
import logmon_config_execution

# Assuming the function get_total_memory_in_gb is defined in a module named `memory_util`


class TestGetTotalMemoryInGB(unittest.TestCase):
    @patch("os.sysconf")
    def test_get_total_memory_in_gb(self, mock_sysconf):
        # Define the values that sysconf will return for SC_PAGE_SIZE and SC_PHYS_PAGES
        mock_sysconf.side_effect = lambda name: {
            "SC_PAGE_SIZE": 4096,  # 4 KB
            "SC_PHYS_PAGES": 262144,  # Number of pages
        }[name]

        # Now, when get_total_memory_in_gb is called, it should use these mocked values
        expected_memory_in_gb = (4096 * 262144) / pow(
            1024, 3
        )  # Calculate expected value in GB

        result = logmon_config_execution.get_total_memory_in_gb()
        self.assertAlmostEqual(result, expected_memory_in_gb)


if __name__ == "__main__":
    unittest.main()
