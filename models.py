from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class UserInput(Base):
    __tablename__ = "user_inputs"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    llm_response = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
