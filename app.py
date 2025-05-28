from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import FileResponse
import pandas as pd
import uuid
import os

app = FastAPI()

def delete_file_after_send(path: str):
    try:
        os.remove(path)
        print(f"Deleted: {path}")
    except Exception as e:
        print(f"Error deleting file {path}: {e}")

@app.post("/generate-csv")
async def generate_csv(request: Request, background_tasks: BackgroundTasks):
    # Step 1: Receive the incoming JSON
    data = await request.json()
    quotes = data.get("quotes", [])

    if not quotes:
        return {"error": "No quotes provided"}
    
    # Step 2: Convert to DataFrame
    df = pd.DataFrame(quotes)

    # Step 3: Save to unique filename
    filename = f"quotes_{uuid.uuid4().hex}.csv"
    df.to_csv(filename, index=False)

    background_tasks.add_task(delete_file_after_send, filename)

    # Step 4: Return the file as a download
    response = FileResponse(filename, media_type="text/csv", filename=filename)

    return response


