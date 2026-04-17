# Enve files in one place for easy access and management
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://vidscribe:vidscribe_local@localhost:5432/vidscribe")
PROJECT_ID = os.getenv("PROJECT_ID", "local-dev")  # Change this when deploying 
PUBSUB_TOPIC = os.getenv("PUBSUB_TOPIC", "vidscribe-jobs")  # Pub/Sub topic name for new jobs
