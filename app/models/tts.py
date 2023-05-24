import os
import requests
import azure.cognitiveservices.speech as speechsdk
from services.utils import removeTags,split_into_sentences
import json
from dotenv import load_dotenv

load_dotenv()

def emotion_to_ssml_tag(emotion):
    """ Map API emotion to Azure TTS emotion tag. """
    mapping = {
        "explain": "friendly",
        "happy": "cheerful",
        "sad": "sad",
        "angry": "angry"
    }
    return mapping[emotion]

def get_emotion(sentence):
    """ Get emotion prediction from API. """
    # url = "www.example.com"
    # payload = {'text': sentence}
    # response = requests.post(url, data=payload).json()
    return "fear"

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

async def text_to_speech(transcript, path_name, actor="en-US-JennyNeural"):
    parsed_text = removeTags(transcript)

    speech_config = speechsdk.SpeechConfig(
        subscription=os.getenv("SPEECH_KEY"),
        region=os.getenv("SPEECH_REGION"),
    )
    voice = actor
    speech_config.speech_synthesis_voice_name = voice
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Split transcript into sentences
    sentences = split_into_sentences(parsed_text)

    # Initialize the SSML text
    ssml_text = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>
    <voice name='{voice}'>"""


    # Process all sentences at once
    emotions = get_emotions(sentences)

    # Process each sentence
    # for sentence in sentences:
    #     emotion = get_emotion(sentence)
    #     ssml_emotion = emotion_to_ssml_tag(emotion)
    #     ssml_text += f"<mstts:express-as style='{ssml_emotion}'>{sentence}</mstts:express-as>"

    # Indicies are always the same in 2 different lists.
    print(f"This is TTS file speaking: \n")
    for sentence, emotion in zip(sentences, emotions):
        print(f"sentence: {sentence}")
        print(f"\n emotion: {emotion}")
        ssml_emotion = emotion_to_ssml_tag(emotion)
        ssml_text += f"<mstts:express-as style='{ssml_emotion}'>{sentence} <break time='1000ms' /></mstts:express-as>"

    ssml_text += "</voice></speak>"
    print(f"final ssml text: \n\n{ssml_text}")
    output_file_path = path_name + ".wav"
    speech_result = speech_synthesizer.speak_ssml_async(ssml_text).get()
    if speech_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        with open(output_file_path, "wb") as audio_file:
            audio_file.write(speech_result.audio_data)
        print(
            f"Speech synthesized with voice '{voice}' and saved to {output_file_path}"
        )
    else:
        print(f"Speech synthesis failed with status: {speech_result.reason}")
