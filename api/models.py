from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class JobRequest(BaseModel):
    video_url: str
    
    
    
    
    
class JobResponse(BaseModel):
    job_id : UUID
    status : str
    created_at : datetime
    video_url : str # Retuned so the user can easily correlate the request and response
    