import os
import json
import csv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class CosineSimilarity:
    def __init__(self, job_descriptions_folder, resumes_folder, model_name):
        self.job_descriptions_folder = job_descriptions_folder
        self.resumes_folder = resumes_folder
        self.model = SentenceTransformer(model_name)
        self.encoded_jds = {}
        self.encoded_resumes = {}
        self.cosine_dict = {}

    def load_encoded_jds(self):
        jd_list = os.listdir(self.job_descriptions_folder)
        for jd in jd_list:
            file_path = os.path.join(self.job_descriptions_folder, jd)
            with open(file_path, "r") as f:
                data = json.load(f)
                clean_data = data.get("clean_data", "")
                encoded_jd = self.model.encode(clean_data)
                self.encoded_jds[jd] = encoded_jd

    def load_encoded_resumes(self):
        resume_list = os.listdir(self.resumes_folder)
        for resume in resume_list:
            file_path = os.path.join(self.resumes_folder, resume)
            with open(file_path, "r") as f:
                data = json.load(f)
                clean_data = data.get("clean_data", "")
                encoded_resume = self.model.encode(clean_data)
                self.encoded_resumes[resume] = encoded_resume

    def calculate_cosine_similarity(self):
        for name, encoded_jd in self.encoded_jds.items():
            for resume, encoded_resume in self.encoded_resumes.items():
                similarity = cosine_similarity(
                    encoded_jd.reshape(1, -1), encoded_resume.reshape(1, -1)
                )
                self.cosine_dict[(name, resume)] = similarity


if __name__ == "__main__":
    job_descriptions_folder = "./data/Processed/JobDescription"
    resumes_folder = "./data/Processed/Resumes"
    model_name = "all-mpnet-base-v2"
    cosine_similarity_obj = CosineSimilarity(
        job_descriptions_folder, resumes_folder, model_name
    )
    cosine_similarity_obj.load_encoded_jds()
    cosine_similarity_obj.load_encoded_resumes()
    cosine_similarity_obj.calculate_cosine_similarity()

    # Exporting the result to a CSV for further Analysis
    csv_file = "cosine_similarity.csv"
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["JD", "Resume", "CosineSimilarity"])

        for (jd, resume), cs in cosine_similarity_obj.cosine_dict.items():
            writer.writerow([jd, resume, cs[0][0]])
