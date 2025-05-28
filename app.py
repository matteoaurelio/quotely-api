from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse
import pandas as pd
import uuid
import os
import asyncio
import io

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Quotely API is running"}


async def delete_file_after_send(path: str):
    try:
        await asyncio.sleep(120)  # Wait for 2 minutes before deleting
        os.remove(path)
        print(f"Deleted: {path}")
    except Exception as e:
        print(f"Error deleting file {path}: {e}")

@app.post("/generate-csv")
async def generate_csv(request: Request, background_tasks: BackgroundTasks):
    try:
        data = await request.json()
        quotes = data.get("quotes", [])

        if not quotes:
            return {"error": "No quotes provided"}

        df = pd.DataFrame(quotes)

        # Write to Render's ephemeral /tmp directory
        filename = f"quotes_{uuid.uuid4().hex}.csv"
        path = f"/tmp/{filename}"
        df.to_csv(path, index=False)

        # Clean up after 2 minutes
        background_tasks.add_task(delete_file_after_send, path)

        return FileResponse(
            path,
            media_type="text/csv",
            filename=filename
        )

    except Exception as e:
        return {"error": str(e)}