# File for structuring the transcript sent to the LLM API. return section titles, body text, and section-start timestamps as a form of structure output

import json
import os
from google import genai
from google.genai import types



from .models import Article, CaptionSegment



# Constants
PROJECT_ID = "vidscribe-491820"                                                           
REGION = "us-central1"         
MODEL_ID = "gemini-2.5-flash-lite"

LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", REGION)

_client: genai.Client | None = None

def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    return _client


RESPONSE_SCHEMA: dict = {
    "type": "object",                                                                     
    "properties": {  
        "title": {"type": "string"},
        "sections": {                                                                     
            "type": "array",
            "items": {                                                                    
                "type": "object",
                "properties": {  
                    "title": {"type": "string"},
                    "body": {"type": "string"}, 
                    "timestamp": {"type": "number"},                                      
                    "subsections": {                
                        "type": "array",                                                  
                        "items": {      
                            "type": "object",
                            "properties": {  
                                "title": {"type": "string"},                              
                                "body": {"type": "string"}, 
                                "timestamp": {"type": "number"}                           
                            },                                 
                            "required": ["title", "body", "timestamp"]
                        }                                                                 
                    }    
                },                                                                        
                "required": ["title", "body", "timestamp", "subsections"]
            }                                                            
        }    
    },   
    "required": ["title", "sections"]
}      

PROMPT_TEMPLATE = """
Accuracy is critical — use only information present in the transcript. Do not add, infer,  or embellish.

  YouTube title (for reference only, may be clickbait): {youtube_title}

  Transcript (format: [seconds] text):
  {transcript}

  Instructions:
  - Write a concise, descriptive article title that reflects the actual content of the
  video. Use the YouTube title as a reference but prefer accuracy over engagement.
  - Divide the transcript into logical sections based on topic shifts. Let the content
  determine the number of sections — do not force a fixed count.
  - For each section write a title, a clear prose summary of that section's content, and the
   approximate timestamp in seconds where that section begins in the video.
  - Do not include information that is not in the transcript.
"""   




                              


def structure_transcript(video_title: str, segments: list[CaptionSegment]) -> Article:
    """ Structure the transcript into an article format with sections and subsections.
    
    Args: 
        video_title: The title of the video, used as a reference for generating the article title.
        segments: List of caption segments extracted from the video, each with start time, end time, and text.
    
    Returns:
        An Article object containing the structured title, sections, and subsections.
    """
    transcript_text = "\n".join(f"[{segment['start']}] {segment['text']}" for segment in segments)
    prompt = PROMPT_TEMPLATE.format(
        youtube_title=video_title,
        transcript=transcript_text
    )
    response = _get_client().models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config= types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=RESPONSE_SCHEMA
        )
    ) 
    article = Article(title="", sections=[])
    if response.candidates and len(response.candidates) > 0:
        json_response : dict = json.loads(response.text)
        article: Article = Article(
            title=json_response["title"],
            sections=json_response["sections"]
        )
    return article

    
    
    
if __name__ == "__main__":                                                                
    from .ingest import extract_captions
                                                                                        
    audio_path = "/tmp/example-job-id.m4a"
    youtube_title = "AI Technical Debt"                                                   
                                                                                        
    captions = extract_captions(audio_path)
    if captions is None:                                                                  
        print("No captions found")                                                        
    else:
        print(f"Found {len(captions)} segments, structuring...")                          
        article = structure_transcript(youtube_title, captions)
        print(f"Title: {article['title']}")                                               
        for section in article['sections']:
            print(f"\n[{section['timestamp']}s] {section['title']}")                      
            print(section['body'][:100], "...")  