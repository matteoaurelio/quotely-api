from fastapi import FastAPI, Request, BackgroundTasks
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import FileResponse, StreamingResponse
import pandas as pd
import uuid
import os
import asyncio
import io
from fastapi import HTTPException
import secrets
from typing import Dict

app = FastAPI()

# In-memory token store: filename → token
file_tokens: Dict[str, str] = {}

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
async def generate_csv(request: Request):
    try:
        data = await request.json()
        quotes = data.get("quotes", [])
        if not quotes:
            return {"error": "No quotes provided"}

        df = pd.DataFrame(quotes)
        filename = f"quotes_{uuid.uuid4().hex}.csv"
        path = f"/tmp/{filename}"
        df.to_csv(path, index=False)

        # Generate secure token for this file
        token = secrets.token_urlsafe(16)
        file_tokens[filename] = token

        return {
            "message": "Your file is ready.",
            "download_url": f"https://quotely-api.onrender.com/files/{filename}?token={token}"
        }

    except Exception as e:
        return {"error": str(e)}
    
@app.get("/files/{filename}")
async def get_file(filename: str, token: str = Query(...)):
    if file_tokens.get(filename) != token:
        raise HTTPException(status_code=403, detail="Invalid or missing token")

    path = f"/tmp/{filename}"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    del file_tokens[filename]

    return FileResponse(
        path,
        media_type="text/csv",
        filename=filename
    )



# @app.post("/generate-csv")
# async def generate_csv(request: Request):
#     try:
#         data = await request.json()
#         quotes = data.get("quotes", [])

#         if not quotes:
#             return {"error": "No quotes provided"}

#         df = pd.DataFrame(quotes)

#         # Set fixed filename
#         filename = "quotes.csv"
#         path = f"/tmp/{filename}"

#         # Save file
#         df.to_csv(path, index=False)

#         # Return download link
#         return {
#             "message": "Your file is ready.",
#             "download_url": f"https://quotely-api.onrender.com/files/{filename}"
#         }

#     except Exception as e:
#         return {"error": str(e)}
    


# @app.get("/files/{filename}")
# async def get_file(filename: str):
#     path = f"/tmp/{filename}"
#     if not os.path.exists(path):
#         raise HTTPException(status_code=404, detail="File not found")

#     return FileResponse(
#         path,
#         media_type="text/csv",
#         filename=filename
#     )

