from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import json
import requests


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Query(BaseModel):
    text: str

def llm_call(query: str, model="gemma:2b-instruct") -> str:
    url = "http://localhost:11434/api/generate"   ##Ollama API endpoint running on port 11434 from local machine
    headers = {"Content-Type": "application/json"}
    data = { "model": model,   ##Model name
            "prompt": query,
            "stream": False}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return json.loads(response.text)['response']
    else:
        return response.text

@app.post("/query")
async def process_query(query: Query):
    try:
        response = llm_call(query.text)
        return JSONResponse(content={"response": response}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Backend (Python using FastAPI)
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import asyncio

# app = FastAPI()

import ollama

def fake_model_stream(query:str):
    stream = ollama.chat(
        model='gemma:2b-instruct',
        messages=[{'role': 'user', 'content': query}],
        stream=True,
    )

    for chunk in stream:
        yield chunk['message']['content']

@app.get("/stream")
async def stream_response(query: str):
    return StreamingResponse(fake_model_stream(query), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

