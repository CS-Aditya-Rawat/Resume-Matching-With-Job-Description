from .parsers import ParseResume
from .ReadPdf import read_single_pdf
import os.path
import pathlib
import time
import json

READ_RESUME_FROM = "./data/Resumes/"
SAVE_DIRECTORY = "./data/Processed/Resumes"


class ResumeProcessor:
    def __init__(self, input_file):
        self.input_file = input_file
        self.input_file_name = os.path.join(READ_RESUME_FROM + self.input_file)

    def process(self) -> bool:
        try:
            resume_dict = self._read_resumes()
            self._write_json_file(resume_dict)
            return True
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False

    def _read_resumes(self) -> dict:
        data = read_single_pdf(self.input_file_name)
        time.sleep(1)
        output = ParseResume(data).get_JSON()
        return output

    def _write_json_file(self, resume_dictionary: dict):
        file_name = str(
            "Resume-"
            + self.input_file.replace(".pdf", "")
            + resume_dictionary["unique_id"]
            + ".json"
        )
        save_directory_name = pathlib.Path(SAVE_DIRECTORY) / file_name
        json_object = json.dumps(resume_dictionary, sort_keys=True, indent=4)
        with open(save_directory_name, "w+") as output:
            output.write(json_object)
