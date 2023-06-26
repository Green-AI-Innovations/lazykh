import os
import azure.cognitiveservices.speech as speechsdk
from services.utilities import removeTags,split_into_sentences
from models.emotion_model import get_emotions
from dotenv import load_dotenv

load_dotenv()

def emotion_to_ssml_tag(emotion):
    """ Map API emotion to Azure TTS emotion tag. """
    mapping = {
        "explain": "friendly",
        "happy": "cheerful",
        "sad": "friendly",
        "angry": "angry"
    }
    return mapping[emotion]


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
    <voice name='{voice}'><prosody rate="5%">"""


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
        ssml_text += f"<mstts:express-as style='{ssml_emotion}'>{sentence}<break time='700ms'/></mstts:express-as>"

    ssml_text += "</prosody></voice></speak>"
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
