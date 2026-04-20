#This is the main file that starts the rest API
import os
from typing import Any
from contextlib import asynccontextmanager
from uuid import UUID
import uuid
from fastapi import FastAPI, File, Request, Depends, Form, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from worker.gcs import upload_video_to_gcs

from .models import JobRequest, JobResponse
from .db import Database, create_job, create_job_with_id
from .worker.gcs import upload_video_to_gcs


#testing at: http://localhost:8000/docs 
@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """Manage datebase connection pool for app lifetime"""
    fastapi_app.state.db = await Database.create()
    yield
    await fastapi_app.state.db.disconnect()
    
    
app = FastAPI(lifespan=lifespan)

def get_db(request: Request) -> Database:
    return request.app.state.db

templates = Jinja2Templates(directory="templates")  


@app.get("/")
def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "submit.html")


@app.post("/jobs")
async def receive_jobs(
    request: Request,
    video_url: str = Form(default=""),
    file: UploadFile | None = File(default=None),
    db: Database = Depends(get_db)
) -> RedirectResponse:
    created_job : JobResponse | None = None
    if(file is not None):
        # Save to temp file
        temp_file_path : str = f"/tmp/{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())
        #Upload the file to GCS and get the public URL
        job_id : uuid.UUID = uuid.uuid4()
        gcs_path = upload_video_to_gcs(temp_file_path, str(job_id))
        video_url = gcs_path
        os.unlink(temp_file_path)  # Clean up the temp file
        created_job = await db.create_job_with_id(video_url, job_id)
    else:    
        created_job = await db.create_job(video_url)
    if created_job is None:  
        return templates.TemplateResponse(request, "submit.html", {"error": "Provide a URL or upload a file."}, status_code=400)
    return RedirectResponse(url=f"/status/{created_job.job_id}", status_code=303)

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


@app.get("/article/{article_id}", response_class = HTMLResponse)
async def article_page(article_id : UUID, request: Request, db: Database = Depends(get_db))-> HTMLResponse:
    """Render a page displaying the article content for the given article ID. The page will show the article title, content, and any associated images. It will also handle the case where the article has expired and display an appropriate message."""
    article_content = await db.get_article_content(article_id)
    return templates.TemplateResponse(request, "article.html", {"article": article_content})
    


@app.get("/status/{job_id}", response_class=HTMLResponse)
async def status_page(request: Request, job_id: UUID) -> HTMLResponse:
    """Render a status page for the given job ID. The page will use JavaScript to poll the /jobs/{job_id} endpoint for status updates and display them to the user. need to coverd the UUID to string."""
    return templates.TemplateResponse(request, "status.html", {"job_id": str(job_id)})




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
