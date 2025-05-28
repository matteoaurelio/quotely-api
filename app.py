from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse
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
async def generate_csv(request: Request):
    # Step 1: Receive the incoming JSON
    data = await request.json()
    quotes = data.get("quotes", [])

    if not quotes:
        return {"error": "No quotes provided"}

    # Step 2: Convert to DataFrame
    df = pd.DataFrame(quotes)

    # Step 3: Convert DataFrame to CSV in memory
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    # Step 4: Stream the CSV directly
    filename = f"quotes_{uuid.uuid4().hex}.csv"
    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

