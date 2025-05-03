import io
from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from pydantic import BaseModel
import requests  # for calling Gemini API or similar
from func import s
from Comparison import kmer_similarity  # Import the comparison function
# Initialize FastAPI app
app = FastAPI()

# Global variable to store uploaded data
df_global = None  # Initialize df_global here

@app.post('/upload-csv/')
async def upload_csv(csv_file: UploadFile = File(...)):
    global df_global  # Use the global variable
    
    # Read the contents of the uploaded file in memory
    contents = await csv_file.read()
    
    # Decode bytes to string and then use StringIO to simulate a file object
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    df_global = df  # Store the DataFrame in the global variable

    # Process the dataframe (just showing columns here as an example)
    return {"filename": csv_file.filename, "columns": df.columns.tolist()}



############################
#step2: generate sequence
@app.get("/generate-sequence/{sample_id}")
async def generate_sequence(sample_id: str):
    df_global =  data_store.get("df")  # Use the global variable

    # Check if the  DataFrame is None 
    if df_global is None:
        raise HTTPException(status_code=400, detail="No data available. Please upload CSV first.")
    
    # Check if the sample_id exists in the DataFrame
    row = df_global[df_global["id"] == sample_id]

    if row.empty:
        raise HTTPException(status_code=404, detail=f"Sample ID {sample_id} not found")
    
    # Extract fields needed for sequence generation
    id = row.iloc[0]["id"]
    region = row.iloc[0]["region"]
    age = row.iloc[0]["age"]
    seed = row.iloc[0]["seed"]

    # Call the function from func.py to generate the DNA sequence
    sequence = s(id, region, age, seed)
    short_sequence = sequence[:500]  # Only return the first 500 characters 

    return {"sample_id": sample_id, "sequence": short_sequence}




############################
#step 3: Comparion

@app.get("/compare-samples/{id1}/{id2}")
async def compare_samples(id1: str, id2: str):
    df_global = data_store.get("df")

    # Check if CSV data is uploaded
    if df_global is None:
        raise HTTPException(status_code=400, detail="No data uploaded. Please upload the CSV first.")

    # Get rows for both IDs
    row1 = df_global[df_global["id"] == id1]
    row2 = df_global[df_global["id"] == id2]

    if row1.empty or row2.empty:
        raise HTTPException(status_code=404, detail="One or both sample IDs not found.")

    # Extract fields for both sequences
    seq1 = s(row1.iloc[0]["id"], row1.iloc[0]["region"], row1.iloc[0]["age"], row1.iloc[0]["seed"])
    seq2 = s(row2.iloc[0]["id"], row2.iloc[0]["region"], row2.iloc[0]["age"], row2.iloc[0]["seed"])

    # Compare the sequences using your function (default k=6)
    result = kmer_similarity(seq1, seq2)

    # Return the result
    return {
        "sample_id_1": id1,
        "sample_id_2": id2,
        "comparison_result": result
    }




##########################  
# Step 4: "Ask Me Anything" model
API_KEY = "AIzaSyDxnUoQ49akvccSZtZuml7mH7Zt8Ug7dHk"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask_gemini(question: Question):  # Accepting raw JSON input (no BaseModel)
    question_text = question.question
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"You are a technical assistant. Provide a formal and concise answer suitable for documentation or project understanding. Context: This is a DNA analysis server that allows CSV upload, sequence generation, and similarity comparison. Now, answer this question: {question_text}"
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Will raise an HTTPError if the response was unsuccessful

        gemini_response = response.json()

        answer = gemini_response['candidates'][0]['content']['parts'][0]['text']
        return {"answer": answer}

    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail="Something went wrong while processing the request.")



