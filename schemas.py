from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserInputCreate(BaseModel):
    input_text: str

class UserInputResponse(BaseModel):
    id: int
    input_text: str
    llm_response: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
