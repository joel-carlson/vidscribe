#This is the main file that starts the rest API
from typing import Any

from fastapi import FastAPI, Request, Depends
from contextlib import asynccontextmanager
from models import JobResponse, JobRequest
from db import Database
from uuid import UUID


@asynccontextmanager
async def lifespan(app: FastAPI) :
    """Manage datebase connection pool for app lifetime"""
    app.state.db = await Database.create()
    yield
    await app.state.db.disconnect()
    
    
app = FastAPI(lifespan=lifespan)

def get_db(request: Request) -> Database:
    return request.app.state.db

@app.get("/")
def home() -> dict[str, str]:
    return {"message" : "entrance to the vidscribe api"}
    


@app.post("/jobs")
async def receive_jobs(job: JobRequest, db: Database = Depends(get_db)) -> JobResponse:
    return await db.create_job(job.video_url)


@app.get("/jobs/{job_id}")
async def return_job_status(job_id : UUID, db: Database = Depends(get_db)) ->str:
    return await db.get_job_status(job_id)

@app.get("/articles/by-job/{job_id}")
async def return_article_id(job_id : UUID, db: Database = Depends(get_db)) -> UUID:
    """Given a job ID, return the associated article ID if the job is completed.                                                                                                                                                                             
        Args:
            job_id: UUID of the job to query."""
    return await db.get_article_id(job_id)

@app.get("/articles/{article_id}")
async def return_article_content(article_id : UUID, db: Database = Depends(get_db)) -> dict[str, Any]:
    """Given an article ID, return the article content and metadata if it exists and has not expired.
        Args:
            article_id: UUID of the article to query."""
    return await db.get_article_content(article_id)


    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
