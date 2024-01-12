from fastapi.testclient import TestClient
from app.endpoint import app

client = TestClient(app)

def test_read_root():
    """ 
    Test the root endpoint.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_filename_audio():
    """
    Test the filename endpoint.
    """
    test_url = "https://youtu.be/jNQXAC9IVRw?si=SdiDOQHjADpoAftR"
    response = client.post("/filename/", json={"url": test_url})
    assert response.status_code == 200

def test_transcribe_audio_endpoint():
    """
    Test the transcribe endpoint.
    """
    test_url = "https://youtu.be/jNQXAC9IVRw?si=SdiDOQHjADpoAftR"
    response = client.post("/transcribe/", json={"url": test_url})
    assert response.status_code == 200
    assert "transcription" in response.json()