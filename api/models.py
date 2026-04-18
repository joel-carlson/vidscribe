from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Any
class JobRequest(BaseModel):
    video_url: str
    
    
    
    
    
class JobResponse(BaseModel):
    job_id : UUID
    status : str
    video_url : str # Retuned so the user can easily correlate the request and response
    created_at : datetime
    expires_at : datetime


class ArticleResponse(BaseModel):
    article_id : UUID
    job_id : UUID
    title : str
    content : dict[str, Any] #since json is key value pairs, we can use a dict to represent the article content and metadata
    created_at : datetime
    expires_at : datetime    
    
    
    