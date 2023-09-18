import json
import uuid
import pathlib
from .parsers import ParseJobDesc
import os
import pandas as pd

READ_JOB_DESCRIPTION_FROM = "data/JobDescription/"
SAVE_DIRECTORY = "data/Processed/JobDescription"


class JobDescriptionProcessor:
    def __init__(self, input_file, no_of_job: int = 1):
        self.input_file = input_file
        self.input_file_name = os.path.join(READ_JOB_DESCRIPTION_FROM, self.input_file)
        self.no_of_job = no_of_job

    def process(self) -> bool:
        data = pd.read_csv(self.input_file_name, nrows=self.no_of_job)
        top_n_data = data.to_dict(orient="records")
        for data in top_n_data:
            try:
                job_desc_dict = ParseJobDesc(data["job_description"]).get_JSON()
                self._write_json_file(job_desc_dict)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        return True

    def _write_json_file(self, job_desc_dictionary: dict):
        file_name = str("JobDescription-" + str(uuid.uuid4()) + ".json")
        save_directory_name = pathlib.Path(SAVE_DIRECTORY) / file_name
        json_object = json.dumps(job_desc_dictionary, sort_keys=True, indent=4)
        with open(save_directory_name, "w+") as outfile:
            outfile.write(json_object)
