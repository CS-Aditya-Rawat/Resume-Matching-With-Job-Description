import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string


# nltk.download('wordnet)
# nltk.download("stopwords")
class TextCleaner:
    def __init__(self, raw_text: str) -> None:
        self.stopwords_set = set(stopwords.words("english") + list(string.punctuation))
        self.lemmatizer = WordNetLemmatizer()
        self.raw_input_text = raw_text

    def clean_text(self) -> str:
        tokens = word_tokenize(self.raw_input_text.lower())
        tokens = [tokens for token in tokens if token not in self.stopwards_set]
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        cleaned_text = " ".join(tokens)
        return cleaned_text
