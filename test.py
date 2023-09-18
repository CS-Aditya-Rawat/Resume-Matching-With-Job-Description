import json
from scripts import ResumeProcessor, JobDescriptionProcessor
from scripts.utils import init_logging_config, get_filenames_from_dir
import logging

init_logging_config()


def read_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


logging.info("Started to Read Data from ./data")

try:
    file_names = get_filenames_from_dir("./data/Resumes")
    logging.info("Reading from Data is now complete.")
except Exception as e:
    logging.error("There are no resumes present in the specified folder.")
    logging.error(f"Exiting from the program. with {e}")
    logging.error("Please add resumes in the Data/Resumes folder and try again.")
    exit(1)

# Parsing the Resumes
logging.info("Starting parsing the resumes.")
logging.info(f"Files: {file_names}")
for file in file_names:
    processor = ResumeProcessor(file)
    success = processor.process()
logging.info("Parsing of the resume is now completed.")

# Parsing the Job Description
logging.info("Started Parsing the Job Description.")
processor = JobDescriptionProcessor("training_data.csv", 15)
success = processor.process()
logging.info("Parsing of the Job Description is now Complete.")
