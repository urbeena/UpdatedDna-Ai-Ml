# 🧬 DNA Analysis API

This project is a FastAPI-powered web service for performing DNA sequence generation,
comparison, and interaction using a Gemini AI model. 
It supports uploading sample data, generating DNA sequences from it, comparing samples based on their sequences, and asking contextual questions.

---

## Features

- Upload sample data (CSV format)
- Generate synthetic DNA sequences using attributes
- Compare two samples and get a similarity score
- Interact with Gemini AI for contextual Q&A
- Swagger UI for interactive testing
- Deployed using Render

---

##  Steps to Use

### 1️⃣ Upload CSV

**Endpoint:**  
`POST /upload-csv/`

**Description:**  
Uploads a CSV file containing sample data with fields like `id`, `region`, `age`, and `seed`.

**Example CSV Content:**
```csv
id,region,age,seed
1,Asia,25,123
2,Europe,30,456


Request (Form-data):
file: Choose your .csv file

Response:
json :{"message": "dataset columns!"}


**2️⃣ Generate DNA Sequence**
Endpoint:
GET /generate-sequence/{sample_id}

Description:
Generates a synthetic DNA sequence from the sample’s region, age, and seed.

Sample Request:
GET /generate-sequence/id_0001

Sample Response:
json{
  "sample_id": 1,
  "sequence": "ATGCGCTAGTTCGATGCC... (500 characters)" # i have limited to 500 because it is a very long sequence unable to load
}


3️⃣ Compare Two Samples
Endpoint:
GET /compare-samples/{id1}/{id2}

Description:
Compares DNA sequences of two samples using k-mer similarity (e.g., common triplets).

Sample Request:
GET /compare-samples/1/2

Sample Response:
json{
  "id1": 1,
  "id2": 2,
  "similarity_score": "85.0%"
}





4️⃣ Ask Gemini AI
Endpoint:
POST /ask

Description:
Ask a contextual or functional question, and get a structured answer via Gemini AI.

Sample Request:
json{
  "question": "How is the DNA sequence generated?"
}

Sample Response:
json{
  "answer": "The DNA sequence is generated using the region, age, and seed of the sample..."
}

Local Setup
Clone the Repository:
git clone https://github.com/urbeena/UpdatedDna-Ai-Ml.git
cd UpdatedDna-Ai-Ml

Install Dependencies:
pip install -r requirements.txt

Run the Application Locally:
uvicorn main:app --reload

Access the API at:
http://127.0.0.1:8000/docs


**🌍 Deployment
Deployed on Render**

Live API URL:
https://updateddna-ai-ml.onrender.com

Swagger Docs:
https://updateddna-ai-ml.onrender.com/docs
NOTE:
The deployed APIs are accessible and working, but there are issues with Step 2 and Step 3
so you can test locally



****📦 Tech Stack**
Python with FastAPI
Pandas for data manipulation
Gemini AI API integration
Render for deployment**



#############OPTIONAL
 **How DNA Similarity is Calculated**********
When comparing two DNA sequences, we use k-mer analysis, where the DNA sequence is broken into overlapping substrings (motifs) of length k. These substrings are known as k-mers.

For example, given a 4-mer comparison:

Sequence 1: agtcagtcagtcagtc
→ 13 k-mers: agtc, gtca, tcag, cagt, ...

Sequence 2: agtcgtacagtctcagt
→ 14 k-mers: agtc, gtcg, tcgt, cgta, ...

Common 4-mers: agtc, cagt, tcag

These common substrings (motifs) represent biological similarities.

We compute:

Jaccard-style similarity:
|common| / max(|A|, |B|) = 3 / 14 ≈ 0.214

Alternative similarity:
|common| / (|A| + |B|) = 3 / 27 ≈ 0.111

This approach gives an alignment-free similarity score, useful for fast sequence comparisons without the need for traditional alignment algorithms.

 Author
GitHub: @urbeena rashid
Email: 10urbeenarashid@gmail.com
