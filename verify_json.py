from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def verify_response():
    print("Sending request to /getMovies...")
    response = client.post("/getMovies", json={"input_text": "I want to watch a warm romance movie with a happy ending."})
    
    if response.status_code != 200:
        print(f"FAILED: Status code {response.status_code}")
        print(response.text)
        return

    data = response.json()
    print("Response received:")
    print(json.dumps(data, indent=2))

    if "recommendations" not in data:
        print("FAILED: 'recommendations' field missing")
        return

    recs = data["recommendations"]
    if not isinstance(recs, list):
        print("FAILED: 'recommendations' is not a list")
        return

    if len(recs) == 0:
        print("WARNING: No recommendations returned (might be expected depending on LLM)")
    else:
        first_rec = recs[0]
        required_keys = ["title", "director", "writer", "cast", "quote", "trigger_warning", "poster_details"]
        missing_keys = [key for key in required_keys if key not in first_rec]
        if missing_keys:
            print(f"FAILED: Missing keys in recommendation: {missing_keys}")
        else:
            print("SUCCESS: Response structure is correct!")

if __name__ == "__main__":
    verify_response()
