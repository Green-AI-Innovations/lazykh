import requests
import json





def get_phonemes(mp3_audio, text_file,filename):
    # Set the URL for the external API
    # takes sound file and text file and the filename
    url = 'http://localhost:8765/transcriptions?async=false'

    # Set the files and data for the HTTP POST request
    files = {'audio': ('example.mp3', mp3_audio),
             'transcript': ('example.txt', text_file)}

    # Send the HTTP POST request to the external API
    response = requests.post(url, files=files)
    json_response = json.loads(response.text)
    # Save the response to a file
    with open('services/temporary/'+filename+'.json', 'w') as f:
        f.write(response.text)

    # Return the response from the external API
    return json_response

