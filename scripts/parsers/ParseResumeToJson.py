import json
from uuid import uuid4
from scripts.Extractor import DataExtractor
from scripts.utils.Utils import TextCleaner
from scripts.KeytermsExtraction import KeytermExtractor


class ParseResume:
    def __init__(self, resume: str):
        self.resume_data = resume
        self.clean_data = TextCleaner.clean_text(self.resume_data)
        self.experience = DataExtractor(self.clean_data).extract_experience()
        self.entities = DataExtractor(self.clean_data).extract_entities()
        self.emails = DataExtractor(self.resume_data).extract_emails()
        self.phones = DataExtractor(self.resume_data).extract_phone_numbers()
        self.years = DataExtractor(self.resume_data).extract_position_year()
        self.key_words = DataExtractor(self.clean_data).extract_particular_words()
        self.keyterms = KeytermExtractor(self.clean_data).get_keyterms_based_on_sgrank()
        self.bi_grams = KeytermExtractor(self.clean_data).bi_gramchunker()
        self.tri_grams = KeytermExtractor(self.clean_data).tri_gramchunker()

    def get_JSON(self) -> dict:
        """
        Returns a dictionary of resume data.
        """
        resume_dictionary = {
            "unique_id": str(uuid4()),
            "resume_data": self.resume_data,
            "clean_data": self.clean_data,
            "experience": self.experience,
            "extracted_keywords": self.key_words,
            "entities": self.entities,
            "phones": self.phones,
            "emails": self.emails,
            "keyterms": self.keyterms,
            "years": self.years,
            "bi_grams": str(self.bi_grams),
            "tri_grams": str(self.tri_grams),
        }

        return resume_dictionary
