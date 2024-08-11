import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai_api():
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        print("API key not found.")
        return

    test_url = "https://api.openai.com/v1/engines"
    headers = {
        "Authorization": f"Bearer {openai_api_key}"
    }

    response = requests.get(test_url, headers=headers)
    if response.status_code == 200:
        print("API key is valid.")
    else:
        print(f"Error: {response.status_code}, {response.json()}")

test_openai_api()
