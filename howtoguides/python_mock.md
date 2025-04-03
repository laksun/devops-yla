import unittest
from unittest.mock import patch, MagicMock, CalledProcessError
from logmon_common import LogmonCommon

class TestLogmonCommon(unittest.TestCase):

    @patch("logmon_common.subprocess.run")
    def test_manage_service_status_success(self, mock_run):
        logmon_common = LogmonCommon()
        mock_run.return_value = MagicMock()  # simulate successful run
        result = logmon_common.manage_service_status(service_name="some_service", action="stop")
        self.assertTrue(result)
        mock_run.assert_called_with(["systemctl", "stop", "some_service"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

    @patch("logmon_common.subprocess.run")
    def test_manage_service_status_process_error(self, mock_run):
        logmon_common = LogmonCommon()
        mock_run.side_effect = CalledProcessError(returncode=1, cmd=["systemctl", "stop", "some_service"])
        result = logmon_common.manage_service_status(service_name="some_service", action="stop")
        self.assertFalse(result)
        mock_run.assert_called_with(["systemctl", "stop", "some_service"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
