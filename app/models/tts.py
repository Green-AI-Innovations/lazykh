import os
import azure.cognitiveservices.speech as speechsdk
from services.utils import removeTags

def text_to_speech(transcript, path_name, actor="en-US-JennyNeural"):


    # Text to convert to speech
    text = removeTags(transcript)

    # Load API key and region from the environment variables
    speech_config = speechsdk.SpeechConfig(
        subscription='803933b47edd4a948d2310aff4fc847f',
        region='westeurope',
    )


    voice = actor
    speech_config.speech_synthesis_voice_name = voice

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)



    # Convert text to speech and save to a file
    output_file_path = path_name + ".wav"
    speech_result = speech_synthesizer.speak_text_async(text).get()
    if speech_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        with open(output_file_path, "wb") as audio_file:
            audio_file.write(speech_result.audio_data)
        print(
            f"Speech synthesized with voice '{voice}' and saved to {output_file_path}"
        )
    else:
        print(f"Speech synthesis failed with status: {speech_result.reason}")

# https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support?tabs=tts#text-to-speech