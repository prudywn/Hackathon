import os
import requests
from aijson import register_action
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@register_action 
def whisper(filename: str) -> str:
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_API_KEY"),
        api_version=os.getenv("AZURE_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_API_BASE")
    )
    
    with open(filename, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            file=audio_file, 
            model="whisper"
        )
    
    # Assuming `result` has a `text` attribute
    return result.text

def generate_unstructured_response(text: str) -> str:
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_API_KEY"),
        api_version=os.getenv("AZURE_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_API_BASE")
    )
    
    response = client.completions.create(
        model="gpt-4",
        prompt=f"Review these meeting notes and identify key decisions and action items: {text}",
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].text.strip()

def structure_response(unstructured_text: str) -> dict:
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_API_KEY"),
        api_version=os.getenv("AZURE_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_API_BASE")
    )
    
    prompt = f"Based on the meeting notes review, what are the key decisions and action items? Summarize the main points: {unstructured_text}"
    
    response = client.completions.create(
        model="gpt-4o",
        prompt=prompt,
        temperature=0
    )
    
    structured_response = response.choices[0].text.strip()
    
    return {
        "key_decisions": [decision.strip() for decision in structured_response.split('\n') if 'Decision' in decision],
        "action_items": [action.strip() for action in structured_response.split('\n') if 'Action' in action]
    }

def format_transcription(text: str) -> str:
    # Split the transcription into sentences based on punctuation
    lines = text.split(',')
    
    # Join the lines with a newline character for better readability
    formatted_text = '\n'.join(line.strip() for line in lines)
    
    return formatted_text

# Example usage
def main():
    audio_file_path = r"C:\Users\User\OneDrive\Documents\Hackathon\src\audio\Rachel Platten - Fight Song (Lyrics).mp3"
    
    # Step 1: Capture voice input and transcribe it
    transcribed_text = whisper(audio_file_path)
    if not transcribed_text:
        print("Transcription failed.")
        return
        
    # Format the transcription for readability
    formatted_text = format_transcription(transcribed_text)
    print("Formatted Transcription:\n", formatted_text)
        
    # Step 2: Generate an unstructured response using Claude
    unstructured_response = generate_unstructured_response(formatted_text)
    
    if not unstructured_response:
        print("Failed to generate unstructured response.")
        return
    
    # Step 3: Structure the response using GPT-4
    structured_response = structure_response(unstructured_response)
    
    # Step 4: Print the structured response in a user-friendly way
    print("\nStructured Response:")
    print("Key Decisions:")
    for decision in structured_response.get("key_decisions", []):
        print(f"- {decision}")
    
    print("\nAction Items:")
    for action in structured_response.get("action_items", []):
        print(f"- {action}")

if __name__ == "__main__":
    main()
