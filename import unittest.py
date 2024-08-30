import unittest
from unittest.mock import patch
from logmon1 import main


class TestMain(unittest.TestCase):

    @patch("logmon1.is_agent_running")
    @patch("logmon1.restart_agent")
    @patch("logmon1.os.system")
    def test_main(self, mock_system, mock_restart_agent, mock_is_agent_running):
        mock_is_agent_running.return_value = False
        main()
        mock_is_agent_running.assert_called_once_with(
            "/etc/init.d/fluentd_user", "status"
        )
        mock_restart_agent.assert_called_once_with(
            "/etc/init.d/fluentd_user", "fluentd_user"
        )
        mock_system.assert_called_with(
            "find /var/log/amazon/ -xdev -path -mmin -60 ! -perm -o=r -ls -exec chmod -c rx {} \\;"
        )
        mock_restart_agent.assert_called_once()


if __name__ == "__main__":
    unittest.main()
