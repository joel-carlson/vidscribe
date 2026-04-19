import asyncpg
import json

import config
from models import Article, ArticleSection


async def assemble_article(job_id: str, article: Article, frame_urls: list[str])-> None:
    """Assemble the final article by combining the structured content with the corresponding frames, and prepare it for storage or delivery.

    Args:
        job_id: Unique identifier for the job, used to organize related data.
        article: The structured article content generated from the video transcript, containing a title and a list of sections with their respective subsections.
        frame_urls: List of public URLs for the extracted frames that correspond to key moments in the video, which will be integrated into the article to enhance its visual appeal and provide context to the readers.
    """
    # Adding the frame URLS to tthe corresponding sections/subsections based on timestamps 
    for section, frame_url in zip(article["sections"], frame_urls):
        # This is done becasue the sections are ordered by their timestamps, so it is an exact match.
        section["frame_url"] = frame_url
        
        
    conn : asyncpg.Connection = await asyncpg.connect(config.DATABASE_URL)
    await conn.execute(
        "INSERT INTO articles (job_id, title, content) VALUES ($1, $2, $3)",
        job_id,
        article["title"],
        json.dumps(article)
    )
    await conn.execute(
        "UPDATE jobs SET status = 'completed' WHERE id = $1",
        job_id
    )
          
          
          
          
if __name__ == "__main__":
    # Example usage
    JOB_ID = "example-job-id"
    ARTICLE = Article(
        title="Example Article Title",
        sections=[
            ArticleSection(
                title="Section 1",
                body="This is the body of section 1.",
                timestamp=10.0,
                subsections=[],
                frame_url=None
            ),
            ArticleSection(
                title="Section 2",
                body="This is the body of section 2.",
                timestamp=30.0,
                subsections=[],
                frame_url=None
            ),
            ArticleSection(
                title="Section 3",
                body="This is the body of section 3.",
                timestamp=60.0,
                subsections=[],
                frame_url=None
            )
        ]
    )
    FRAME_URLS = [
        "https://storage.googleapis.com/your-bucket/example-job-id/frame_10.0.jpg",
        "https://storage.googleapis.com/your-bucket/example-job-id/frame_30.0.jpg",
        "https://storage.googleapis.com/your-bucket/example-job-id/frame_60.0.jpg"
    ]
    
    print("Assembling article...")
    import asyncio
    asyncio.run(assemble_article(JOB_ID, ARTICLE, FRAME_URLS))
    print("Article assembled and stored in database.")