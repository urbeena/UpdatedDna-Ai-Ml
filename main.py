
import io
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from pydantic import BaseModel
import requests  # For calling Gemini API
from func import s
from Comparison import kmer_similarity

# Constants
CSV_FILE_PATH = "data.csv"

# Initialize FastAPI app
app = FastAPI()


# Helper function to load the CSV
def load_csv():
    if not os.path.exists(CSV_FILE_PATH):
        return None
    return pd.read_csv(CSV_FILE_PATH)


#################################
# Upload CSV
@app.post("/upload-csv/")
async def upload_csv(csv_file: UploadFile = File(...)):
    contents = await csv_file.read()
    decoded = contents.decode("utf-8")

    # Save file persistently
    with open(CSV_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(decoded)

    df = pd.read_csv(io.StringIO(decoded))
    return {"filename": csv_file.filename, "columns": df.columns.tolist()}


#################################
# Generate DNA sequence for sample ID
@app.get("/generate-sequence/{sample_id}")
async def generate_sequence(sample_id: str):
    df = load_csv()
    if df is None:
        raise HTTPException(status_code=400, detail="CSV not found. Please upload it first.")

    row = df[df["id"] == sample_id]
    if row.empty:
        raise HTTPException(status_code=404, detail=f"Sample ID {sample_id} not found.")

    id = row.iloc[0]["id"]
    region = row.iloc[0]["region"]
    age = row.iloc[0]["age"]
    seed = row.iloc[0]["seed"]

    sequence = s(id, region, age, seed)
    return {"sample_id": sample_id, "sequence": sequence[:500]}  # Limit response


#################################
# Compare 2 samples
@app.get("/compare-samples/{id1}/{id2}")
async def compare_samples(id1: str, id2: str):
    df = load_csv()
    if df is None:
        raise HTTPException(status_code=400, detail="CSV not found. Please upload it first.")

    row1 = df[df["id"] == id1]
    row2 = df[df["id"] == id2]

    if row1.empty or row2.empty:
        raise HTTPException(status_code=404, detail="One or both sample IDs not found.")

    seq1 = s(row1.iloc[0]["id"], row1.iloc[0]["region"], row1.iloc[0]["age"], row1.iloc[0]["seed"])
    seq2 = s(row2.iloc[0]["id"], row2.iloc[0]["region"], row2.iloc[0]["age"], row2.iloc[0]["seed"])

    result = kmer_similarity(seq1, seq2)

    return {
        "sample_id_1": id1,
        "sample_id_2": id2,
        "comparison_result": result
    }


#################################
# Ask Gemini endpoint
API_KEY = "AIzaSyDxnUoQ49akvccSZtZuml7mH7Zt8Ug7dHk"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask_gemini(question: Question):
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"You are a technical assistant. Provide a formal and concise answer suitable for documentation or project understanding. Context: This is a DNA analysis server that allows CSV upload, sequence generation, and similarity comparison. Now, answer this question: {question.question}"
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_URL, headers=headers, json=data)
        response.raise_for_status()

        gemini_response = response.json()
        answer = gemini_response['candidates'][0]['content']['parts'][0]['text']
        return {"answer": answer}

    except Exception as e:
        print("Gemini API Error:", str(e))
        raise HTTPException(status_code=500, detail="Failed to get response from Gemini.")
