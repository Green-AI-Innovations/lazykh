import requests
import json
import os
import re



def emotion_to_lazykh_tag(emotion):
    """ Map API emotion to lazykh tag. """
    # lazky kh tags explain,happy,sad,angry,confused,rq
    mapping = {
        "explain": "<explain>",
        "happy": "<happy>",
        "sad": "<sad>",
        "angry": "<angry>",
    }
    return mapping[emotion]


def get_emotions(sentences):
    """ Get emotion prediction from API. """
    url = os.getenv('API_URL')
    # Token API
    token = os.getenv('API_HEADER_AUTH')
    auth_header = {'Authorization': f'Bearer {token}'}
    # Create and submit a request using the auth header
    headers = auth_header
    # Add content type header
    headers.update({'Content-Type':'application/json'})
    payload = json.dumps({'data': sentences})
    payload = bytes(payload,encoding = 'utf8')
    response = requests.post(url, payload, headers=headers)
    print(f"response from API is: \n\n {response.json()}")
    return response.json()

def emotion_classfy(transcript, temp_path, randomeFilename):
    sentences = re.split(r'[.!?]\s+', transcript)
    classifiedText = ""
    emotions = get_emotions(sentences)
    # for sentence in sentences:
    #     emotion = get_emotion(sentence)
    #     lazykh_tag = emotion_to_lazykh_tag(emotion)
    #     classifiedText += f"{lazykh_tag} {sentence}"
    print(f"This is fake classifier method speaking: \n")
    for sentence, emotion in zip(sentences, emotions):
        print(f"sentence: {sentence}")
        print(f"\n emotion: {emotion}")
        lazykh_tag = emotion_to_lazykh_tag(emotion)
        classifiedText += f"{lazykh_tag} {sentence}. \n"

    with open(temp_path + randomeFilename + '.txt', 'w') as f:
        f.write(classifiedText)

    return classifiedText
