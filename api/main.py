#This is the main file that starts the rest API
import uvicorn
from fastapi import FastAPI, Request, Depends
from contextlib import asynccontextmanager
from models import JobResponse, JobRequest
from db import Database


@asynccontextmanager
async def lifespan(app: FastAPI) :
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

    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
