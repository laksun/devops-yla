# import unittest
# from unittest.mock import mock_open, patch
# from QuestionEngine import QuestionEngine


# class TestQuestionEngine(unittest.TestCase):

#     def setUp(self):
#         # We will patch the open function in the QuestionEngine module, so when it tries to open a file, it uses our mocks
#         self.patcher = patch(
#             "QuestionEngine.open", new_callable=mock_open, read_data="Sample text"
#         )
#         self.mock_open = self.patcher.start()

#         # Create an instance of the QuestionEngine class
#         # The file paths passed here are irrelevant since the open function is mocked
#         self.qe = QuestionEngine("path/to/book.txt", "path/to/words.txt")

#     def tearDown(self):
#         # Stop patching 'open'
#         self.patcher.stop()

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

#     @patch("QuestionEngine.open")
#     def test_question_generator(self, mock_open):
#         # Mock the return values of the file read methods
#         mock_open.side_effect = [
#             mock_open.return_value.__enter__.return_value,  # First call for book file
#             mock_open.return_value.__enter__.return_value.read.return_value,
#             "This is a sample text.",  # Mocked book file content
#             mock_open.return_value.__enter__.return_value,  # Second call for words file
#             mock_open.return_value.__enter__.return_value.read.return_value,
#             "sample\ntext",  # Mocked words file content
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
