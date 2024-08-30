import unittest
from unittest.mock import patch
import os

# Assuming set_environ is defined in logmon1.py
from logmon1 import set_environ


class TestSetEnviron(unittest.TestCase):

    @patch("platform.version")
    def test_set_environ_ubuntu(self, mock_version):
        mock_version.return_value = "Ubuntu"
        set_environ()
        self.assertEqual(os.environ["REQUESTS_CA_BUNDLE"], "/etc/ssl/certs/a.crt")
        self.assertEqual(os.environ["SSL_CERT_FILE"], "/etc/ssl/certs/a.crt")

    @patch("platform.version")
    def test_set_environ_non_ubuntu(self, mock_version):
        mock_version.return_value = "Non-Ubuntu"
        set_environ()
        self.assertEqual(os.environ["REQUESTS_CA_BUNDLE"], "/etc/ssl/certs/b.crt")
        self.assertEqual(os.environ["SSL_CERT_FILE"], "/etc/ssl/certs/b.crt")
