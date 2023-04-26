import os
import azure.cognitiveservices.speech as speechsdk


def text_to_speech(transcript, path_name, actor="en-US-JennyNeural"):
    # Load API key and region from the environment variables
    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ.get("SPEECH_KEY"),
        region=os.environ.get("SPEECH_REGION"),
    )

    voice = actor
    speech_config.speech_synthesis_voice_name = voice

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Text to convert to speech
    text = transcript

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


string_var = """The quick brown fox jumped over the lazy dog and then ran away but he was caught by the farmer and put in a cage."""
from app.models.pos import segment_text

string_var = segment_text(string_var)
print(string_var)
text_to_speech(string_var, "test")
