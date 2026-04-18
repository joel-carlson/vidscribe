import whisper
import yt_dlp
import os

from api.worker.ingest import CaptionSegment







WHISPER_MODEL_SIZE = "small"
WHISPER_TASK = "transcribe"  

def transcribe_with_whisper(video_path: str) -> list[CaptionSegment]:
    """
    Use OpenAI's Whisper model to transcribe the audio from a video file. 
    The audio will need to be extracted from the video file first. Done using ffmpeg.
    Args:
        video_path: Path to the video file to transcribe.
    Returns:
        A list of CaptionSegment objects
    """    








