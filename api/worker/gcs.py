from google.cloud import storage
from google.auth.credentials import AnonymousCredentials

from config import GCS_BUCKET_NAME, GCS_ENDPOINT_URL, GCS_PUBLIC_URL_BASE, GCS_PROJECT_ID


_client : storage.Client = storage.Client(credentials=AnonymousCredentials(), project=GCS_PROJECT_ID, client_options={"api_endpoint": GCS_ENDPOINT_URL})

def upload_frames_to_gcs(frame_paths: list[str], job_id: str) -> list[str]:
    """Upload extracted frames to Google Cloud Storage and return their public URLs.

    Args:
        frame_paths: List of local file paths to the extracted frames.
        job_id: Used to organize frames in GCS under a common prefix.

    Returns:
        List of public URLs for the uploaded frames.
    """
    # Get bucket from the client
    bucket: storage.Bucket = _client.bucket(GCS_BUCKET_NAME)
    if not bucket.exists():
        bucket.create()                                                                                                                
                         
    public_urls: list[str] = []
    for frame_path in frame_paths:
        frame_name = frame_path.split("/")[-1]
        blob = bucket.blob(f"{job_id}/{frame_name}")
        blob.upload_from_filename(frame_path)
        public_urls.append(f"{GCS_PUBLIC_URL_BASE}{job_id}/{frame_name}")
        
    
    return public_urls

    
    
if __name__ == "__main__":
    # Example usage requries running the frames.py first to generate the frame files
    FRAME_PATHS = ["/tmp/example-job-id/frame_10.0.jpg", "/tmp/example-job-id/frame_30.0.jpg", "/tmp/example-job-id/frame_60.0.jpg"]  # These should be the paths to the extracted frames
    JOB_ID = "example-job-id"
    
    print("Uploading frames to GCS...")
    public_urls = upload_frames_to_gcs(FRAME_PATHS, JOB_ID)
    print("Public URLs for uploaded frames:")
    for url in public_urls:
        print(url)