import argparse
import logging
import os

from pytube import YouTube
import whisper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL = whisper.load_model("base")

def download_audio(url):
    """
    Download audio from the given URL.
    Args:
        url (str): The URL of the YouTube video.
    Returns:
        str: The filename of the downloaded audio.
    """
    logger.info("Downloading audio from %s", url)
    yt = YouTube(url)
    logger.info("Title: %s", yt.title)
    logger.info("Length: %s", yt.length)
    
    stream = yt.streams.filter(only_audio=True).first()
    stream.download()

    return stream.default_filename

def transcribe_audio(filename):
    """
    Transcribe the given audio file.
    Args:
        filename (str): The filename of the audio file.
    Returns:
        str: The transcription of the audio file.
    """
    logger.info("Transcribing %s", filename)
    transcription = MODEL.transcribe(filename, fp16=False)
    clean_up(filename)
    return transcription

def convert_to_mp3(filename: str) -> str:
    """
    Convert the given file to mp3 format.
    Args:
        filename (str): The filename of the file to be converted.
    Returns:
        str: The new filename of the converted file.
    """
    logger.info("Converting %s to mp3", filename)
    new_filename = filename[:-4] + ".mp3"
    os.rename(filename, new_filename)
    logger.info("Converted %s to mp3", filename)
    return new_filename

def clean_up(filename):
    """
    Clean up the given file.
    Args:
        filename (str): The filename of the file to be cleaned up.
    """
    logger.info("Cleaning up %s", filename)
    os.remove(filename)
    logger.info("Cleaned up %s", filename)

def main(args):
    """
    Main function to download and transcribe audio from YouTube.
    Args:
        args (list): Command line arguments.
    """
    parser = argparse.ArgumentParser(description="Download and transcribe audio from YouTube")
    parser.add_argument("url", help="URL of YouTube video")
    parser.add_argument("-o", "--output", help="Output file for transcription", default='output.txt')
    args = parser.parse_args(args)

    filename = download_audio(args.url)
    filename = convert_to_mp3(filename)
    try:
        transcription = transcribe_audio(filename)
    except Exception as e:
        logger.error("Transcription failed")
        logger.error(e)
        transcription = ""

    if args.output:
        with open(args.output, "w", encoding= "utf-8") as f:
            f.write(transcription['text'])

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
