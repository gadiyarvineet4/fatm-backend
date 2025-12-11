from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db, Base
import models
import schemas
from services.groq_service import get_groq_response
# Renamed from prompt_engine per file name
from prompt import PromptEngineer

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FATM Backend")

# Mock DB for demonstration - User should replace this with actual data source
DB = {
    "sets": {
        "romance_warm": {"description": "Low stakes, happy endings.", "ids": [1, 2]},
        "comedy_dark": {"description": "Funny but with dark themes.", "ids": [3, 4]},
        "sci_fi_futuristic": {"description": "Space travel and future tech.", "ids": [5, 6]}
    }
}

prompt_engine = PromptEngineer(DB["sets"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FATM Backend"}

@app.post("/getMovies", response_model=schemas.UserInputResponse)
def get_movies(input_data: schemas.UserInputCreate, db: Session = Depends(get_db)):
    """
    Accepts string input, gets response from Groq, and saves to database.
    """
    # 1. Generate System Prompt (Using Recommendation Prompt for Testing)
    # system_prompt = prompt_engine.generate_system_prompt()
    system_prompt = prompt_engine.generate_recommendation_prompt()
    
    # 2. Get response from Groq
    llm_response = get_groq_response(input_data.input_text, system_prompt)

    # 2. Save to database
    db_input = models.UserInput(
        input_text=input_data.input_text,
        llm_response=llm_response
    )
    db.add(db_input)
    db.commit()
    db.refresh(db_input)

    return db_input
