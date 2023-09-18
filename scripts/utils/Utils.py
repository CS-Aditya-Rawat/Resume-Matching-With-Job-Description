import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import spacy

nlp = spacy.load("en_core_web_md")

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
        lemmatizer = WordNetLemmatizer()
        text = re.sub(r"\n", " ", text)
        text = re.sub(
            r"[\u0000-\u001F\u007F-\u009F\u00AD\u0600-\u0604\u200B-\u200F\u2028-\u202F\u2060-\u206F\uFEFF]",
            "",
            text,
        )
        text = TextCleaner.remove_emails_link(text)
        tokens = TextCleaner.remove_stopwords(text)
        tokens = word_tokenize(text.lower())
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
        cleaned_text = " ".join(tokens)

        doc = nlp(cleaned_text)
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
