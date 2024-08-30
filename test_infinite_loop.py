import unittest
from unittest.mock import patch

# Import the function you want to test
from infinite_loop import infinite_loop_function


class TestInfiniteLoopFunction(unittest.TestCase):

    @patch("builtins.print")  # Mock print to prevent actual printing
    @patch(
        "time.sleep", side_effect=InterruptedError
    )  # Mock time.sleep to break the loop
    def test_infinite_loop_function(self, mock_sleep, mock_print):
        with self.assertRaises(InterruptedError):
            infinite_loop_function()

        # Verify that the loop started and printed something
        mock_print.assert_called_with("Loop iteration: 0")


if __name__ == "__main__":
    unittest.main()
