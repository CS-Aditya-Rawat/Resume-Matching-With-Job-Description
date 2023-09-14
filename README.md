<div align="center">

# 📄Resume Matching with the Job Description 💼
</div>

## Process
### Resume Processing is almost completed.
1. Extraction of Experience, position, year, skills, name, email, phone and all the links.
1. Extracting all kind of keywords.
1. Extracting key terms and rank them using **textacy sgrank**

1. Added the code to extract the bi-grams and tri-grams.
    - Bi-grams: Pairs of consecutive words or tokens in a text. 
    - Tri-grams: Sequences of three consecutive words or tokens in a text

### Job Description processing is in work.
1. Write Now Job description is in csv. So, I am reading a single row at a time and planed to show the top 5 resumes who have highest cosine similarity with that Job Description.