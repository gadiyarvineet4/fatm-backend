from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import schemas
import json
from services.groq_service import get_groq_response
# Renamed from prompt_engine per file name
from prompt import PromptEngineer



app = FastAPI(title="FATM Backend")

# CORS Configuration
origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
def get_movies(input_data: schemas.UserInputCreate):
    """
    Accepts string input, gets response from Groq.
    """
    # 1. Generate System Prompt (Using Recommendation Prompt for Testing)
    # system_prompt = prompt_engine.generate_system_prompt()
    system_prompt = prompt_engine.generate_recommendation_prompt()
    
    # 2. Get response from Groq
    llm_response = get_groq_response(input_data.input_text, system_prompt)

    # 3. Parse LLM response to get recommendations
    recommendations = []
    note = None
    try:
        response_data = json.loads(llm_response)
        # Handle case where llm_response isn't perfectly structured or keys differ
        recommendations = response_data.get("recommendations", [])
        note = response_data.get("note")
    except json.JSONDecodeError:
        print("Error decoding JSON from LLM")
        recommendations = []

    return schemas.UserInputResponse(
        id=None, # No ID since not saved to DB
        input_text=input_data.input_text,
        llm_response=llm_response,
        created_at=None, # No created_at since not saved to DB
        recommendations=recommendations,
        note=note
    )
