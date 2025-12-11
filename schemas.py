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
    movie_poster: Optional[str] = ""

class UserInputResponse(BaseModel):
    id: int
    input_text: str
    llm_response: Optional[str] = None
    recommendations: Optional[List[MovieRecommendation]] = []
    created_at: datetime

    class Config:
        orm_mode = True
