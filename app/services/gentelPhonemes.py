import requests
import json
from services.utils import removeTags


def get_phonemes(path, filename):
    try:

        # Set the URL for the external API
        url = 'http://gentle:8765/transcriptions?async=false'

        # Read the transcript file
        with open(path + filename + '.txt', 'rb') as transcript_file:
            transcript = transcript_file.read()

        print("removeTags from transcript")
        transcript=removeTags(transcript)

        # Read the audio file
        with open(path + filename+'.wav', 'rb') as audio_file:
            audio = audio_file.read()

        print(transcript)

        # Set the files and data for the HTTP POST request
        files = {'audio': ('example.wav', audio, 'audio/wav'),
                'transcript': ('example.txt', transcript)}

        # Send the HTTP POST request to the external API
        response = requests.post(url, files=files, timeout=60)
        json_response = json.loads(response.text)

        # Save the response to a file
        with open('services/temporary/'+filename+'.json', 'w') as f:
            f.write(response.text)

        # Return the response from the external API
        return json_response
    
    except requests.exceptions.RequestException as e:
        print("An error occurred during the HTTP request:", str(e))
        # You can handle the error here, log it, or raise a custom exception
    except (IOError, json.JSONDecodeError) as e:
        print("An error occurred while reading or writing files:", str(e))
        # You can handle the error here, log it, or raise a custom exception
    except Exception as e:
        print("An unexpected error occurred:", str(e))
        # You can handle the error here, log it, or raise a custom exception

    return None  # Return None if an error occurred