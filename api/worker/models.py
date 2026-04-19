from typing import TypedDict

class CaptionSegment(TypedDict):
    start: float
    end: float
    text: str

class SubSection(TypedDict):                                                              
    title: str                                                                            
    body: str                                                                             
    timestamp: float

class ArticleSection(TypedDict):                                                          
    title: str
    body: str                                                                             
    timestamp: float
    subsections: list[SubSection]

class Article(TypedDict):
    title: str
    sections: list[ArticleSection]