import azure.cognitiveservices.speech as speechsdk


def text_to_speech(transcript, path_name, actor="en-US-JennyNeural"):
    # Load API key and region from the .env file
    api_key = (
        "af6821f1ff0d4b99a6fd062c5301727a"  # we will integrate azure key vault soon
    )
    region = "westeurope"

    # Configure the TTS client
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)

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
