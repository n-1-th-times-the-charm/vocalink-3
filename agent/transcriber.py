import assemblyai as aai
import os
from agent.constants import FILE_PATH
from agent.graph import vocalink_graph

aai.settings.api_key = os.getenv("AAI_API_KEY")
global file
file = open(FILE_PATH, "a+")
file.seek(0)

def on_open(session_opened: aai.RealtimeSessionOpened):
  print("Session ID:", session_opened.session_id)

def on_data(transcript: aai.RealtimeTranscript):
  if not transcript.text:
    return

  if isinstance(transcript, aai.RealtimeFinalTranscript):
    print("Recent Transcript:", transcript.text)
    file.seek(0)
    current_file_state = file.read()
    print("Current file state: ", current_file_state)
    vocalink_graph.invoke({"user_input": transcript.text, "current_file_state": current_file_state})

def on_error(error: aai.RealtimeError):
  print("An error occured:", error)

def on_close():
  print("Closing Session")

transcriber = aai.RealtimeTranscriber(
  on_data=on_data,
  on_error=on_error,
  sample_rate=16_000,
  on_open=on_open,
  on_close=on_close,
)
transcriber.connect()
try:
    microphone_stream = aai.extras.MicrophoneStream(sample_rate=16_000)
    transcriber.stream(data=microphone_stream)
except Exception as e:
    print(e)
    transcriber.close()
transcriber.close()