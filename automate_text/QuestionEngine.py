from typing import List
import re
import os

# create comment to how to use the methods


class QuestionEngine:
    def __init__(self, book_file_path: str, words_file_path: str):
        self.book_file_path = book_file_path
        self.words_file_path = words_file_path

    def read_file_from_local(self) -> str:
        with open(self.book_file_path, "r") as file:
            return file.read()

    def read_words_from_file(self) -> List[str]:
        """
        Reads words from a file and returns a list of strings.

        Args:
            words_file_path (str): The path to the words file.

        Returns:
            List[str]: A list of words read from the file.
        """

        words: List[str] = []

        with open(self.words_file_path, "r") as file:
            for line in file:
                word: str = line.strip()  # Remove any surrounding whitespace/newlines
                words.append(word)

        return words

    def parse_text_to_sentences(self, text: str) -> list:
        # Parse the text to sentences
        sentences = re.split(
            r"(?<=[.!?])\s+", text.replace("\n", " ").replace("\r", "")
        )
        return sentences

    def question_generator(self) -> List[dict]:
        # Read the text from the file
        text: str = self.read_file_from_local()

        # Parse the text to sentences
        sentences: List[str] = self.parse_text_to_sentences(text)

        # Read the word list from the file
        words: List[str] = self.read_words_from_file()

        # Filter the sentences that contain the words
        questions = []
        for sentence in sentences:
            for word in words:
                if word in sentence:
                    questions.append({"sentence": sentence, "word": word})
                    break

        return questions


# create an instance of the class and call question_generator method
# Get the absolute path of the current directory
def main():
    current_dir = os.path.abspath(os.getcwd())

    # Construct the absolute paths for the book file and words file
    book_file_path = os.path.abspath(
        os.path.join(current_dir, "../data/books/pride_and_prejudice.txt")
    )
    words_file_path = os.path.abspath(
        os.path.join(current_dir, "../data/words/6000.txt")
    )

    # Create an instance of the class and call question_generator method
    qe = QuestionEngine(book_file_path, words_file_path)
    questions = qe.question_generator()
    print(questions)
    questions = qe.question_generator()
    print(questions)


if __name__ == "__main__":
    main()
