import requests
import json
import wave



def get_phonemes(audio_path, transcript,filename):
    # Set the URL for the external API
    # takes sound file and text file and the filename
    url = 'http://127.0.0.1/transcriptions?async=false'

    audio_file = wave.open(audio_path + filename, 'rb')
    audio = audio_file.readframes(audio_file.getnframes())

    # Set the files and data for the HTTP POST request
    files = {'audio': ('example.wav',audio),
             'transcript': ('example.txt', transcript)}

    # Send the HTTP POST request to the external API
    response = requests.post(url, files=files)
    json_response = json.loads(response.text)
    # Save the response to a file
    with open('services/temporary/'+filename+'.json', 'w') as f:
        f.write(response.text)

    # Return the response from the external API
    return json_response

