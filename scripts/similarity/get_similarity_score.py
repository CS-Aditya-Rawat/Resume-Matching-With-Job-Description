import json
import logging
import os
from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Batch

load_dotenv()
logging.basicConfig(
    filename="similarity_score.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("similarity_score.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


def read_doc(path):
    with open(path) as f:
        try:
            data = json.load(f)
        except Exception as e:
            logger.error(f"Error reading JSON file: {e}")
            data = {}
        return data


class QdrantSearch:
    def __init__(self, resumes, jd):
        self.cohere_key = os.environ.get("COHERE_KEY")
        self.qdrant_key = os.environ.get("QDRANT_KEY")
        self.qdrant_url = os.environ.get("QDRANT_URL")
        self.resumes = resumes
        self.jd = jd
        self.cohere = cohere.Client(self.cohere_key)
        self.collection_name = "resume_collection"
        self.qdrant = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_key,
        )
        vector_size = 4096
        print(f"Collection name={self.collection_name}")
        self.qdrant.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=vector_size, distance=models.Distance.COSINE
            ),
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def get_embedding(self, text):
        try:
            embeddings = self.cohere.embed([text], "large").embeddings
            return list(map(float, embeddings[0])), len(embeddings[0])
        except Exception as e:
            self.logger.error(f"Error getting embeddings: {e}", exc_info=True)

    def update_qdrant(self):
        vectors = []
        ids = []
        for i, resume in enumerate(self.resumes):
            vector, size = self.get_embedding(resume)
            vectors.append(vector)
            ids.append(i)

        try:
            self.qdrant.upsert(
                collection_name=self.collection_name,
                points=Batch(
                    ids=ids,
                    vectors=vectors,
                    payloads=[{"text": resume} for resume in self.resumes],
                ),
            )
        except Exception as e:
            self.logger.error(
                f"Error upserting the vectors to the qdrant collection: {e}",
                exc_info=True,
            )

    def search(self):
        vector, _ = self.get_embedding(self.jd)

        hits = self.qdrant.search(
            collection_name=self.collection_name, query_vector=vector, limit=30
        )
        results = []
        for hit in hits:
            result = {"text": str(hit.payload)[:30], "score": hit.score}
            results.append(result)

        return results

    def get_similarity_score(resume_string, job_description_string):
        logger.info("Started getting similarity score")
        qdrant_search = QdrantSearch([resume_string], job_description_string)
        qdrant_search.update_qdrant()
        search_result = qdrant_search.search()
        logger.info("Finished getting similarity score")
        return search_result


if __name__ == "__main__":

    def find_path(folder_name):
        curr_dir = os.getcwd()
        while True:
            if folder_name in os.listdir(curr_dir):
                return os.path.join(curr_dir, folder_name)
            else:
                parent_dir = os.path.dirname(curr_dir)
                if parent_dir == "/":
                    break
                curr_dir = parent_dir
        raise ValueError(f"Folder '{folder_name}' not found.")

    cwd = find_path("resume-matching")
    READ_RESUME_FROM = os.path.join(cwd, "data", "Processed", "Resumes")
    READ_JOB_DESCRIPTION_FROM = os.path.join(cwd, "data", "Processed", "JobDescription")
    with open(
        READ_RESUME_FROM + "\\Resume-10030015d193d501-3e8f-48d2-81f3-d79a872d85ee.json",
        "r",
    ) as f:
        data = json.load(f)
        resume_keywords = data["extracted_keywords"]
    with open(
        READ_JOB_DESCRIPTION_FROM + "\\JobDescription-training_data.json", "r"
    ) as f:
        data = json.load(f)
        job_description_keywords = data["extracted_keywords"]

    resume_string = " ".join(resume_keywords)
    jd_string = " ".join(job_description_keywords)
    final_result = QdrantSearch.get_similarity_score(resume_string, jd_string)
    for r in final_result:
        print(r)
