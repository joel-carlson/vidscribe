import whisper
import os
import torch
from models import CaptionSegment







WHISPER_MODEL_SIZE = "small"
WHISPER_TASK = "transcribe"  

def _get_device() -> str:
    if torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def transcribe_with_whisper(audio_path: str, language: str | None = None) -> list[CaptionSegment]:
    """
    Use OpenAI's Whisper model to transcribe the audio from the downloaded audiofile. 
    
    
    Using the small model for a good balance of speed and accuracy, Can be adjusted based on needs and resource constraints. 
    Args:           
        audio_path: Path to the audio file to transcribe.
        language: BCP-47 language code (e.g. "en") or None to auto-detect.
    Returns:
        A list of CaptionSegment objects
    """    

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found at path: {audio_path}")
    model = whisper.load_model(WHISPER_MODEL_SIZE, device=_get_device())
    result: dict = model.transcribe(audio_path, task=WHISPER_TASK, language=language, verbose=False)
    return [
        CaptionSegment(start=seg["start"], end=seg["end"], text=seg["text"].strip())
        for seg in result["segments"]
    ] 
    
    
if __name__ == "__main__":
    print("Testing Whisper transcription on sample audio...")
    # Testing on the sample audio file
    segments = transcribe_with_whisper("/tmp/example-job-id.m4a", language="en")
    print("Transcription complete. Sample segments:")
    for seg in segments[:5]:  # Print the first 5 segments for verification
        print(f"{seg['start']:.2f} --> {seg['end']:.2f}: {seg['text']}")
        