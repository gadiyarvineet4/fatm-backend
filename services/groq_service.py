import os
import time
import logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def get_groq_response(user_input: str, system_prompt: str = None) -> str:
    """
    Sends the user input to Groq API and returns the response.
    Optionally accepts a system_prompt to guide the LLM.
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    messages.append({"role": "user", "content": user_input})

    try:
        start_time = time.time()
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
        )
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"Groq API response time: {duration:.4f} seconds")
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return "Error: Unable to fetch response from AI."
