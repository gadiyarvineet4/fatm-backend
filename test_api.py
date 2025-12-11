import requests
import json

# URL of the FastAPI application
URL = "http://127.0.0.1:8000/getMovies"

def test_api():
    payload = {
        "input_text": "Tell me a joke about Python programming."
    }
    
    try:
        print(f"Sending POST request to {URL}...")
        response = requests.post(URL, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print("\nSuccess!")
            print(f"ID: {data['id']}")
            print(f"Input: {data['input_text']}")
            print(f"Response: {data['llm_response']}")
        else:
            print(f"\nFailed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the server. Make sure uvicorn is running.")

if __name__ == "__main__":
    test_api()
