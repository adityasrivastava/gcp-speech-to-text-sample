"""
Main application to:
1. Capture speech and transcribe to text (Speech-to-Text)
2. Translate the transcribed text (Translate)
3. Convert translated text to speech (Text-to-Speech)
"""
from stt1 import listen_print_loop, MicrophoneStream, RATE, CHUNK
from google.cloud import speech
from gcp_translate import translate_text
from google.cloud import texttospeech


def get_speech_text():
    """Capture audio and return transcribed text."""
    language_code = "en-US"
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )
    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )
        responses = client.streaming_recognize(streaming_config, requests)
        text = listen_print_loop(responses)
    return text


def synthesize_speech(text, language_code="en-US", filename="output.mp3"):
    """Convert text to speech and save as MP3."""
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    # Map short language codes to TTS codes (add more as needed)
    tts_language_map = {
        "en": "en-US",
        "es": "es-ES",
        "fr": "fr-FR",
        "de": "de-DE",
        "hi": "hi-IN",
        # Add more mappings as needed
    }
    tts_language_code = tts_language_map.get(language_code, "en-US")
    voice = texttospeech.VoiceSelectionParams(
        language_code=tts_language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open(filename, "wb") as out:
        out.write(response.audio_content)
    print(f'Audio content written to file "{filename}"')


def main():
    print("Speak now...")
    text = get_speech_text()
    print(f"Transcribed: {text}")
    target_language = input("Enter target language code (e.g., 'es' for Spanish): ").strip()
    translation = translate_text(text, target_language=target_language)
    translated_text = translation[0]['translatedText']
    print(f"Translated: {translated_text}")
    synthesize_speech(translated_text, language_code=target_language, filename="output.mp3")
    print("Translated audio saved as output.mp3")


if __name__ == "__main__":
    main()
