# import unittest
# from unittest.mock import mock_open, patch
# from QuestionEngine import QuestionEngine


# class TestQuestionEngine(unittest.TestCase):

#     def setUp(self):
#         # Create an instance of the QuestionEngine class
#         self.qe = QuestionEngine("path/to/book.txt", "path/to/words.txt")

#     @patch("builtins.open", new_callable=mock_open, read_data="Hello, World!")
#     def test_read_file_from_local(self, mock_file):
#         # Mocking the file path
#         file_path = "/path/to/file.txt"

#         # Call the function
#         result = self.qe.read_file_from_local()

#         # Verify the file was opened correctly
#         mock_file.assert_called_once_with(file_path, "r")

#         # Verify the result
#         self.assertEqual(result, "Hello, World!")

#     def test_parse_text_to_sentences(self):
#         text = "Hello! How are you? I'm fine."
#         expected_result = ["Hello!", "How are you?", "I'm fine."]
#         result = self.qe.parse_text_to_sentences(text)
#         self.assertEqual(result, expected_result)

#     import unittest

#     @patch("builtins.open")
#     def test_question_generator(self, mock_open):
#         # Mock the return value of the file read methods
#         mock_open.side_effect = [
#             mock_open.return_value.__enter__.return_value,
#             "This is a sample text.",
#             mock_open.return_value.__enter__.return_value,
#             ["sample", "text"],
#         ]

#         # Call the question_generator method
#         questions = self.qe.question_generator()

#         # Assert that the questions list is correct
#         expected_questions = [
#             {"sentence": "This is a sample text.", "word": "sample"},
#             {"sentence": "This is a sample text.", "word": "text"},
#         ]
#         self.assertEqual(questions, expected_questions)


# if __name__ == "__main__":
#     unittest.main()
