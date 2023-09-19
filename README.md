<div align="center">

# 📄Resume Matching with the Job Description 💼
</div>

## How to Install
Follow these steps to setup the environment and run the application.
1. Fork the repository [fork](https://github.com/CS-Aditya-Rawat/Resume-Matching-With-Job-Description/fork).
1. Clone the forked repository
    ```
    git clone https://github.com/<YOUR-USERNAME>/Resume-Matcher.git
    cd Resume-Matching-With-Job-Description
    ```
1. Create a Python Virtual Environment.
    ```python -m venv .venv```

1. Activate the Virtual Environment.
    - On Windows
        ```
        .venv\Scripts\activate
        ```
    - On macOS and Linux.
        ```
        source .venv/bin/activate
        ```
1. Install Dependencies:
    ```
    pip install -r requirements.txt
    ```    

1. Prepare Data:
    - Resumes: Place Your resume in PDF format in the `data/Resumes` folder.Remove any existing contents in this folder.
    - Job Description: The Job is currently Place in the CSV in `data/JobDescription`, So follow that format.

1. Parse Resumes and JDs to JSON:
    ```
    py test.py
    ```
## Extraction of Information from Resumes and JDs
### Resume Processing is completed.
1. Extraction of Experience, position, year, skills, name, email, phone and all the links.
1. Extracting all kind of keywords.
1. Extracting key terms and rank them using **textacy sgrank**

1. Added the code to extract the bi-grams and tri-grams.
    - Bi-grams: Pairs of consecutive words or tokens in a text. 
    - Tri-grams: Sequences of three consecutive words or tokens in a text

### Job Description processing is completed.
1. Write Now, I extract only the top 15 JDs from the given JDs CSV file.

## For Finding Similarities between Resume and JD:
### Used Sentence Transformer
1. I have used the state-of-the-art natural language processing model, specifically, the 'all-mpnet-base-v2' model from the Sentence Transformer library.
1. The model helps to compute semantic similarity between job descriptions and resumes. By encoding both JDs and resumes into high-dimensional vector representations, I can accurately measure the cosine similarity between these vectors
### Added Qdrant Vector Database with Cohere
1. Cohere is the LLM model, I used it to create embedding for the extracted keywords in both resume and the job description.
1. store the embeddings in the Qdrant Vector Database, utilizing the Cosine Distance as the distance metric. This choice facilitates the efficient calculation of cosine similarity, a key component in my project's natural language processing tasks.
## Resources I used:

1. [Cohere Docs](https://docs.cohere.com/docs/semantic-search)
1. [Qdrant Vector Database](https://qdrant.tech/documentation/tutorials/search-beginners/)
1. [S.Bert](https://www.sbert.net/docs/pretrained_models.html)
## Problems I faced during this project:
1. Cleaning and preprocessing text data is a little bit challenging, including removing special characters, stop words, and dealing with different text formats.

    - **Solution**: Implement a robust data preprocessing pipeline using libraries like textacy and spaCy to handle tokenization, stop word removal, and use Regex for other common text cleaning tasks.

1. When using Sentence Transformers or Cohere API, I face issues with embeddings having different dimensions for resumes and job descriptions.

    - **Solution**: Ensure that the embeddings for both resumes and job descriptions have the same dimensionality. I addressed this by resizing the embeddings to align with the expected dimensions for accurate similarity calculations.

1. I encountered an issue when applying cosine similarity to the embedded resumes and job descriptions. After encoding them, the model provided me with a numpy array of shape (n,). When attempting to compute cosine similarity, I received an error message instructing me to "reshape your data either using array.reshape(-1, 1) if your data has a single feature or array.reshape(1, -1) if it contains a single sample."

    - **Solution**: To resolve this, I chose to reshape the data with the dimensions (1, -1). I opted for (1, -1) because my goal was to compare one job description to one resume at a time.