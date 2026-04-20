from typing import TypedDict

class CaptionSegment(TypedDict):
    """Represents a segment of captions with start and end timestamps and the corresponding text."""
    start: float
    end: float
    text: str

class SubSection(TypedDict): 
    """Represents a subsection within an article section, containing a title, body text, and a timestamp indicating where it appears in the video."""                                                          
    title: str                                                                            
    body: str                                                                             
    timestamp: float
    frame_url: str | None  # Optional field to hold the URL of the corresponding frame, if available
class ArticleSection(TypedDict):                                                          
    """Represents a section within an article, containing a title, body text, a timestamp indicating where it appears in the video, and a list of subsections that further break down the content of the section.

    Args:
        TypedDict (_type_): _description_
    """
    title: str
    body: str                                                                             
    timestamp: float
    subsections: list[SubSection]
    frame_url: str | None  # Optional field to hold the URL of the corresponding frame, if available

class Article(TypedDict):
    """Represents a structured article generated from a video transcript, containing a title and a list of sections, where each section may have its own subsections.

    Args:
        TypedDict (_type_): _description_
    """
    title: str
    sections: list[ArticleSection]
    
