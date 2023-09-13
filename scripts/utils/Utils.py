import re
import spacy

nlp = spacy.load("en_core_web_sm")

REGEX_PATTERNS = {
    "email_pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "phone_pattern": r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
    "link_pattern": r"\b(?:https?://|www\.)\S+\b",
}


class TextCleaner:
    """
    A class for cleaning a text by removing specific patterns.
    """

    def remove_emails_link(text):
        """
        Clean the input text by removing Email, Phone, Link.

        Args:
            text (str): The input text to clean.

        Returns:
            str: The cleaned text.
        """
        for pattern in REGEX_PATTERNS:
            text = re.sub(REGEX_PATTERNS[pattern], "", text)
        return text

    def clean_text(text):
        """
        Clean the input text by removing specific patterns.

        Args:
            text(str): The input text to clean.

        Returns:
            str: The cleaned text.
        """
        text = TextCleaner.remove_emails_link(text)
        doc = nlp(text)
        for token in doc:
            if token.pos == "PUNCT":
                text = text.replace(token.text, "")

        return str(text)

    def remove_stopwords(text):
        """
        Clean the input text by removing stopwords

        Args:
            text (str): The input text to clean.

        Returns:
            str: The cleaned text
        """
        doc = nlp(text)
        for token in doc:
            if token.is_stop:
                text = text.replace(token.text, "")
        return text


class CountFrequency:
    def __init__(self, text):
        self.text = text
        self.doc = nlp(text)

    def count_frequency(self):
        """
        Count the frequency of words in the input text.

        Returns:
            dict: A dicionary with the words as keys and the frequency as the values.
        """
        pos_freq = {}
        for token in self.doc:
            if token.pos_ in pos_freq:
                pos_freq[token.pos_] += 1
            else:
                pos_freq[token.pos_] = 1

        return pos_freq
