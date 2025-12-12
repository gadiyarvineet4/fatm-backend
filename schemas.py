from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class UserInputCreate(BaseModel):
    input_text: str

class MovieRecommendation(BaseModel):
    title: str
    director: str
    writer: str
    cast: str
    quote: str
    trigger_warning: Optional[str] = ""
    poster_details: Optional[str] = ""

class UserInputResponse(BaseModel):
    id: Optional[int] = None
    input_text: str
    llm_response: Optional[str] = None
    recommendations: Optional[List[MovieRecommendation]] = []
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
