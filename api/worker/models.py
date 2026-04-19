from typing import TypedDict

class CaptionSegment(TypedDict):
    start: float
    end: float
    text: str