import uuid
from scripts.Extractor import DataExtractor
from scripts.utils.Utils import TextCleaner
from scripts.KeytermsExtraction import KeytermExtractor

SAVE_DIRECTORY = "../../data/Processed/JobDescription"


class ParseJobDesc:
    def __init__(self, job_desc: str) -> None:
        self.job_desc_data = job_desc
        self.clean_data = TextCleaner.clean_text(self.job_desc_data)
        self.entities = DataExtractor(self.clean_data).extract_entities()
        self.key_words = DataExtractor(self.clean_data).extract_particular_words()
        self.keyterms = KeytermExtractor(self.clean_data).get_keyterms_based_on_sgrank()
        self.bi_grams = KeytermExtractor(self.clean_data).bi_gramchunker()
        self.tri_grams = KeytermExtractor(self.clean_data).tri_gramchunker()

    def get_JSON(self) -> dict:
        """
        Returns a dictionary of job dictionary data.
        """
        job_desc_dictionary = {
            "unique_id": str(uuid.uuid4()),
            "job_desc_data": self.job_desc_data,
            "clean_daat": self.clean_data,
            "entities": self.entities,
            "extracted_keywords": self.key_words,
            "keyterms": self.keyterms,
            "bi_grams": str(self.bi_grams),
            "tri_grams": str(self.tri_grams),
        }
        return job_desc_dictionary
