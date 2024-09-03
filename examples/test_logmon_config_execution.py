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


def test_get_total_memory_in_gb(monkeypatch):
    # Mocking os.sysconf to return specific values for SC_PAGE_SIZE and SC_PHYS_PAGES
    def mock_sysconf(name):
        if name == "SC_PAGE_SIZE":
            return 4096  # 4 KB page size
        elif name == "SC_PHYS_PAGES":
            return 262144  # 256 MB total physical pages

    # Apply the monkeypatch
    monkeypatch.setattr(os, "sysconf", mock_sysconf)

    # Expected result calculation
    expected_memory_in_bytes = 4096 * 262144
    expected_memory_in_gb = expected_memory_in_bytes / pow(1024, 3)

    # Call the function and check the result
    result = get_total_memory_in_gb()
    assert result == pytest.approx(expected_memory_in_gb, rel=1e-6)


if __name__ == "__main__":
    unittest.main()
