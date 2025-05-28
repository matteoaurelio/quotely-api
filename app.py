from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import FileResponse
import pandas as pd
import uuid
import os
import asyncio

app = FastAPI()



async def delete_file_after_send(path: str):
    try:
        await asyncio.sleep(120)  # Wait for 2 minutes before deleting
        os.remove(path)
        print(f"Deleted: {path}")
    except Exception as e:
        print(f"Error deleting file {path}: {e}")


@app.get("/")
def root():
    return {"status": "Quotely API is running"}

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
    path = f"./{filename}"
    df.to_csv(path, index=False)

    # Step 4: Schedule deletion after 2 min
    background_tasks.add_task(delete_file_after_send, path)

    # Step 5: Return file for direct download
    return FileResponse(
        path,
        media_type="text/csv",
        filename=filename
    )

