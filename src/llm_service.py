import requests
import os

# def generate_meeting_review(user_speech):
#     claude_api_key = os.getenv('CLAUDE_API_KEY')
#     # Simulate API call to Claude-3-5 for generating meeting review
#     meeting_notes = f"Review of the meeting notes: {user_speech}"
#     print("Generated Meeting Review:", meeting_notes)
#     return meeting_notes

def generate_meeting_review(user_speech):
    claude_api_key = os.getenv('CLAUDE_API_KEY')
    claude_url = "https://api.anthropic.com/v1/completions"

    headers = {
        "Authorization": f"Bearer {claude_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "prompt": f"Review these meeting notes and identify key decisions and action items: {user_speech}",
        "model": "claude-3-5-sonnet-20240620",
        "temperature": 1
    }

    response = requests.post(claude_url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result.get("choices")[0].get("text", "")
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def structure_meeting_review(meeting_notes):
    gpt4o_api_key = os.getenv('GPT4O_API_KEY')
    gpt4o_url = "https://api.openai.com/v1/completions"

    headers = {
        "Authorization": f"Bearer {gpt4o_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "prompt": f"Based on the meeting notes review, what are the key decisions and action items? Summarize the main points: {meeting_notes}",
        "model": "gpt-4o",
        "temperature": 0
    }

    response = requests.post(gpt4o_url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        # Assuming the API returns structured data in JSON
        return result.get("choices")[0].get("text", "")
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# def structure_meeting_review(meeting_notes):
#     gpt4o_api_key = os.getenv('GPT4O_API_KEY')
#     # Simulate API call to GPT-4o for structuring the response
#     structured_response = {
#         "key_decisions": ["Decision 1", "Decision 2"],
#         "action_items": ["Action Item 1", "Action Item 2"]
#     }
#     print("Structured Meeting Review:", structured_response)
#     return structured_response
