from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import WebSocket
from dotenv import load_dotenv
import os
import requests
import uvicorn
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
from agent.utils import get_expert
from agent.streaming_graph import vocalink_graph
from agent.constants import FILE_PATH
import os
from fastapi import WebSocket
from agent.transcriber import *

load_dotenv()
AAI_API_KEY = os.getenv("AAI_API_KEY")
if not AAI_API_KEY:
    raise ValueError("AAI_API_KEY environment variable not set")

os.environ["AAI_API_KEY"] = AAI_API_KEY

app = FastAPI()
if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, "w") as f:
        pass
origins = [
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:3000",
    "*",  
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get-token")
def get_token():
    url = "https://api.assemblyai.com/v2/realtime/token"
    headers = {
        "authorization": AAI_API_KEY,
        "content-type": "application/json"
    }
    body = {"expires_in": 36000}
    response = requests.post(url, json=body, headers=headers)
    if response.status_code == 200:
        token = response.json().get("token")
        return {"token": token}
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to generate token")

@app.websocket("/api/audio-stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    transcriber = aai.RealtimeTranscriber(
        on_data=on_data,
        on_error=on_error,
        sample_rate=16_000
    )
    transcriber.connect()
    try:
        while True:
            audio_chunk = await websocket.receive_bytes()
            transcriber.stream(data=audio_chunk)
    except Exception as e:
        print(f"Error in WebSocket: {e}")
    finally:
        transcriber.close()

class SteamDocumentRequest(BaseModel):
    text: str

@app.post("api/stream/document")
async def stream_response(request: SteamDocumentRequest):
    user_input = request.text
    expert = get_expert(user_input)
    with open(FILE_PATH, "r") as file:
        current_file_state = file.read()
    output = ""
    async def generate():
        nonlocal output
        yield json.dumps({"expert": expert, "output": ""}) + "\n"
        for message_chunk, _ in vocalink_graph.stream(
            {"user_input": user_input, "current_file_state": current_file_state, "expert": expert, "output": output},
            stream_mode="messages",
        ):
            if message_chunk.content:
                output += message_chunk.content
                yield json.dumps({"expert": expert, "output": message_chunk.content}) + "\n"
    return StreamingResponse(
        generate(), 
        media_type="application/x-ndjson"
    )

class StreamWebRequest(BaseModel):
    text: str
    current_file_state: str

@app.post("/api/stream/web")
async def stream_web_response(request: StreamWebRequest):
    user_input = request.text
    current_file_state = request.current_file_state
    expert = get_expert(user_input)
    output = ""
    async def generate():
        nonlocal output
        yield json.dumps({"expert": expert, "output": ""}) + "\n"
        for message_chunk, _ in vocalink_graph.stream(
            {"user_input": user_input, "current_file_state": current_file_state, "expert": expert, "output": output},
            stream_mode="messages",
        ):
            if message_chunk.content:
                output += message_chunk.content
                yield json.dumps({"expert": expert, "output": message_chunk.content}) + "\n"
    return StreamingResponse(
        generate(), 
        media_type="application/x-ndjson"
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)