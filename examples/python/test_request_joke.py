import unittest

from unittest.mock import MagicMock, patch

from request_joke import len_joke, get_joke

import requests
from requests.exceptions import Timeout


class TestRequestJoke(unittest.TestCase):

    @patch("request_joke.get_joke")
    def test_len_joke(self, mock_get_joke):
        mock_get_joke.return_value = "Chuck Norris can divide by zero."
        self.assertEqual(len_joke(), 32)

    def test_get_joke(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                "value": "Chuck Norris can divide by zero."
            }
            self.assertEqual(get_joke(), "Chuck Norris can divide by zero.")

            mock_get.return_value.status_code = 400
            self.assertEqual(get_joke(), "No jokes")

    @patch("request_joke.requests")
    def test_fail_get_joke(self, mock_requests):
        mock_response = MagicMock(status_code=403)
        mock_response.json.return_value = {"value": "Chuck Norris can divide by zero."}
        mock_requests.get.return_value = mock_response

        self.assertEqual(get_joke(), "No jokes")

    @patch("request_joke.requests")
    def test_get_joke_timeout_exception(self, mock_requests):
        mock_requests.exceptions = requests.exceptions

        mock_requests.get.side_effect = Timeout("Seems that server is down")

        self.assertEqual(get_joke(), "No jokes")
