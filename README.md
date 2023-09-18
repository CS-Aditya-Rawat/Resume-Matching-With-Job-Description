<div align="center">

# 📄Resume Matching with the Job Description 💼
</div>

## Extract of Information from Resumes and JDs
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
### 1. Added Qdrant Vector Database with Cohere
1. Cohere is the nlp model help to create embedding for the extracted keywords in both resume and the job description.
1. I am storing the embeddings in the Qdrant Vector Database, it helps me in the semantic search.
### 2. Used Sentence Transformer
1. I have used the state-of-the-art natural language processing model, specifically, the 'all-mpnet-base-v2' model from the Sentence Transformer library.
1. I used the model to compute semantic similarity between job descriptions and resumes. By encoding both JDs and resumes into high-dimensional vector representations, I can accurately measure the cosine similarity between these vectors
## Problems I faced during this project:
1. I encountered an issue when applying cosine similarity to the embedded resumes and job descriptions. After encoding them, the model provided me with a numpy array of shape (n,). When attempting to compute cosine similarity, I received an error message instructing me to "reshape your data either using array.reshape(-1, 1) if your data has a single feature or array.reshape(1, -1) if it contains a single sample."

    **Solution**: To resolve this, I chose to reshape the data with the dimensions (1, -1). I opted for (1, -1) because my goal was to compare one job description to one resume at a time.