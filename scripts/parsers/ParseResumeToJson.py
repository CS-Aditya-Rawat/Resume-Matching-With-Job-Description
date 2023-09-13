import json
from uuid import uuid4
from scripts.Extractor import DataExtractor
from scripts.utils.Utils import TextCleaner


class ParseResume:
    def __init__(self, resume: str):
        self.resume_data = resume
        self.clean_data = TextCleaner.clean_text(self.resume_data)
        self.experience = DataExtractor(self.clean_data).extract_experience()
        # self.emails = DataExtractor(self.resume_data).extract_
        self.phones = DataExtractor(self.resume_data).extract_phone_numbers()

    def get_JSON(self) -> dict:
        """
        Returns a dictionary of resume data.
        """
        resume_dictionary = {
            "unique_id": str(uuid4()),
            "resume_data": self.resume_data,
            "clean_data": self.clean_data,
            "experience": self.experience,
            "phones": self.phones,
        }

        return resume_dictionary
