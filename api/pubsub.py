import json
from google.cloud.pubsub_v1 import PublisherClient
from uuid import UUID
from config import PROJECT_ID, PUBSUB_TOPIC



def publish_job(video_url : str, job_id : UUID) -> None:
    """Publish a new job to the Pub/Sub queue so that it can be picked up by a worker for processing.
                                                                                                                                                                                                                                            
        Args:
            video_url: URL of the video to process.
            job_id: UUID of the newly created job.
    """
    job_data = {
        "video_url": video_url,
        "job_id": str(job_id)
    }

    # Encode the job data
    message: bytes = json.dumps(job_data).encode("utf-8")
    
    #Building the topic path
    topic_path = f"projects/{PROJECT_ID}/topics/{PUBSUB_TOPIC}"
    
    # Create a Publisher client and publish the message
    publisher: PublisherClient = PublisherClient()
    publisher.publish(topic_path, message)
     
    