import unittest
from unittest.mock import patch, MagicMock, call
import os
import subprocess
import logging
import time

# Assuming main and other functions are imported from the module
from logmon1 import main, set_environ, is_agent_running, restart_agent


class TestMainFunction(unittest.TestCase):

    @patch("logmon1.time.sleep", return_value=None)  # Prevent actual sleeping
    @patch("logmon1.os.system")  # Mock os.system to avoid real system calls
    @patch(
        "logmon1.subprocess.call", return_value=0
    )  # Mock subprocess call to always return 0
    @patch("logmon1.LogmonCommon")
    @patch(
        "logmon1.is_agent_running", side_effect=[False, False, True]
    )  # Simulate agent stopping and starting
    def test_main(
        self,
        mock_is_agent_running,
        mock_LogmonCommon,
        mock_subprocess_call,
        mock_os_system,
        mock_time_sleep,
    ):
        # Setup the mock LogmonCommon instance and its attributes
        mock_logmon_common_instance = mock_LogmonCommon.return_value
        mock_logmon_common_instance.fluentd_config.fluentd_user = "fluentd"
        mock_logmon_common_instance.fluentd_config.var_log_path = "/var/log/amazon/"

        # Run the main function with a loop breaker
        with patch("builtins.input", side_effect=[None, KeyboardInterrupt]):
            try:
                main()
            except KeyboardInterrupt:
                pass  # Expected to break the loop

        # Assertions to ensure the main loop did execute and functions were called
        self.assertEqual(
            mock_is_agent_running.call_count, 3
        )  # Check that is_agent_running was called 3 times
        self.assertTrue(
            mock_subprocess_call.called
        )  # Ensure subprocess.call was triggered
        self.assertTrue(mock_os_system.called)  # Ensure os.system was called

        # Verify specific calls if needed
        mock_os_system.assert_any_call("pkill -9 -f fluentd")
        mock_subprocess_call.assert_any_call("/etc/init.d/fluentd stop", shell=True)
        mock_subprocess_call.assert_any_call("/etc.init.d/fluentd start", shell=True)


if __name__ == "__main__":
    unittest.main()
