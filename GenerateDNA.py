from fastapi import APIRouter, HTTPException
from func import s
from globals import data_store  # Import the shared dict

router = APIRouter()

@router.get("/generate-sequence/{sample_id}")
def generate_sequence(sample_id: str):
    df = data_store.get("df")  #  Get DataFrame

    if df is None:
        raise HTTPException(status_code=400, detail="No data available. Please upload CSV first.")
    
    print(f"Data in df_global: {df['df'].head()}") 

    row = df[df["id"] == sample_id]

    if row.empty:
        raise HTTPException(status_code=404, detail=f"Sample ID {sample_id} not found")

    id = row.iloc[0]["id"]
    region = row.iloc[0]["region"]
    age = row.iloc[0]["age"]
    seed = row.iloc[0]["seed"]

    sequence = s(id, region, age, seed)
    short_sequence = sequence[:500]  # Only return the first 500 characters
    return {"sample_id": sample_id, "sequence": short_sequence}
