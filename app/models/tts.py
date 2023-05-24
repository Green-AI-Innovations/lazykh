import os
import requests
import azure.cognitiveservices.speech as speechsdk
from services.utils import removeTags,split_into_sentences

def emotion_to_ssml_tag(emotion):
    """ Map API emotion to Azure TTS emotion tag. """
    mapping = {
        "fear": "terrified"
    }
    return mapping.get(emotion, "neutral")

def get_emotion(sentence):
    """ Get emotion prediction from API. """
    # url = "www.example.com"
    # payload = {'text': sentence}
    # response = requests.post(url, data=payload).json()
    return "fear"

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

    # Process each sentence
    for sentence in sentences:
        emotion = get_emotion(sentence)
        ssml_emotion = emotion_to_ssml_tag(emotion)
        ssml_text += f"<mstts:express-as style='{ssml_emotion}'>{sentence}</mstts:express-as>"

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
