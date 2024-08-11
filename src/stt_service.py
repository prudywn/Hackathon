import requests
import os

def convert_speech_to_text(audio_file_path):
    whisper_api_key = os.getenv('WHISPER_API_KEY')  # Ensure this is correctly set
    whisper_url = "https://api.openai.com/v1/audio/transcriptions"

    headers = {
        "Authorization": f"Bearer {whisper_api_key}",
    }

    try:
        with open(audio_file_path, "rb") as audio_file:
            files = {'file': audio_file}
            response = requests.post(whisper_url, headers=headers, files=files)

        if response.status_code == 200:
            result = response.json()
            return result.get("text", "")
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
    except FileNotFoundError:
        print(f"Error: The file '{audio_file_path}' was not found.")
        return None

def main():
    audio_file_path = r"C:\Users\User\OneDrive\Documents\Hackathon\src\audio\Rachel Platten - Fight Song (Lyrics).mp3"
    transcription = convert_speech_to_text(audio_file_path)
    print(transcription)

if __name__ == "__main__":
    main()
