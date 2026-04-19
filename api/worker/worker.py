from google.cloud import pubsub_v1
import asyncio
from threading import Event
import json



from config import PUBSUB_SUBSCRIPTION, GCS_PROJECT_ID
from ingest import download_video, download_audio, extract_captions
from cache import cache_transcript
from assembly import assemble_article
from transcription import transcribe_with_whisper
from structuring import structure_transcript
from frames import extract_frames
from gcs import upload_frames_to_gcs



async def process_job(video_url: str, job_id: str) -> None: 
    """Main function to process a video URL and generate an article. 
        This orchestrates the workflow.
    Args:
        video_url: URL of the video to process.
        job_id: Unique identifier for the job, used to organize related data and track progress.
    """
    # Step 1: Download the audio and captions
    audio_path, video_title = download_audio(video_url, job_id)
    captions = extract_captions(audio_path)
    if captions is None:
        print("No captions found, creating with whisper")
        captions = transcribe_with_whisper(audio_path, language="en")
    #Step 2: Cache the captions and video path for later use in assembly
    cache_transcript(job_id, captions)
    #step 3: Download the video for frame extraction
    video_path = download_video(video_url, job_id)
    
    #Step 4: Structure the captions into an article format
    article: dict = structure_transcript(video_title, captions)
    time_stamps: list[float] = [s["timestamp"] for s in article["sections"]]
    #Step 5: Extract frames from the video at key timestamps
    frames: list[str]  = extract_frames(video_path, time_stamps, job_id)
    #Step 6: Upload the frames to cloud storage and get their public URLs
    frame_urls : list[str]= upload_frames_to_gcs(frames, job_id)
    #Step 7: Assemble the final article
    await assemble_article(job_id, article, frame_urls)
    
    
# runs continuously to listen for new jobs and process them
def listen() ->None:
    """
        Listens for new video processing jobs on a Pub/Sub topic and triggers the processing workflow for each incoming job.
    """
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(GCS_PROJECT_ID, PUBSUB_SUBSCRIPTION)
       
    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        print(f"Received message: {message.data}")
        data : dict = json.loads(message.data)
        video_url : str = data["video_url"]
        job_id : str = data["job_id"]
        print(f"Processing job {job_id} for video {video_url}")
        asyncio.run(process_job(video_url, job_id)) 
        message.ack()

    # strarts the background thread that polls pub/sub
    subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")
    # Keep the main thread alive to listen for messages
    Event().wait()  # Wait indefinitely until the process is killed



if __name__ == "__main__":
    VIDEO_URL = "https://www.youtube.com/watch?v=DgXV8QSlI4U"
    JOB_ID = "example-job-id"
    asyncio.run(process_job(VIDEO_URL, JOB_ID))