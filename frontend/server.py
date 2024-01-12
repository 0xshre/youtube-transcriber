import streamlit as st
import requests
import fastapi
import re
from fastapi.testclient import TestClient
from app.endpoint import app

client = TestClient(app)

youtube_url_pattern = re.compile(r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.be)\/.+$")


def is_valid_youtube_url(url):
    """Check if the provided URL is a valid YouTube URL."""
    return youtube_url_pattern.match(url) is not None

st.title("YouTube Transcriber")
st.write("Copy and paste a YouTube link to get started!")
st.write("This app uses OpenAI's Whisper to transcribe YouTube videos.")

st.write("## Enter YouTube URL")
url = st.text_input("URL", "")

if url:
    # Check if URL is valid
    if not is_valid_youtube_url(url):
        st.write("Please enter a valid YouTube URL.")
    else:
        st.write("## Transcription")
        # Add a loading indicator while waiting for the backend
        with st.spinner("Transcribing audio..."):
            try:
                # Get transcription from backend API from an endpoint called "transcribe"
                # response = requests.post("http://127.0.0.1:8000/transcribe", json={"url": url}, timeout=10)
                
                # Or, use the TestClient to make requests if you're running the backend locally 
                response = client.post("/transcribe", json={"url": url})
                
                # Check if the request was successful
                if response.status_code == 200:
                    transcription = response.json().get("transcription", "No transcription found")
                    st.write(transcription)
                else:
                    st.error(f"Error: {response.status_code}")
            except requests.exceptions.Timeout:
                # Handle the timeout exception
                st.error("Request timed out. Please try again.")
            except requests.exceptions.RequestException as e:
                # Handle other possible exceptions
                st.error(f"An error occurred: {e}")
else:
    st.write("Please enter a YouTube URL.")

# footer
st.write("---")
st.write("Made by [Shreyas Prasad](https://shreyasprasad.com)")