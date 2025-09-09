"""
Text-to-Speech service using Google Cloud Text-to-Speech API
"""
from google.cloud import texttospeech
from typing import Optional
import os


class TextToSpeechService:
    """Service for converting text to speech using Google Cloud Text-to-Speech API"""
    
    def __init__(self, language_code: str = "en-US", voice_name: str = None):
        """
        Initialize the Text-to-Speech service
        
        Args:
            language_code: Language code for speech synthesis (e.g., "en-US", "es-ES")
            voice_name: Specific voice name (optional, uses default for language if None)
        """
        self.client = texttospeech.TextToSpeechClient()
        self.language_code = language_code
        self.voice_name = voice_name
    
    def synthesize_text(self, text: str, output_file_path: str) -> bool:
        """
        Convert text to speech and save as audio file
        
        Args:
            text: Text to convert to speech
            output_file_path: Path where to save the audio file
            
        Returns:
            True if synthesis was successful, False otherwise
        """
        try:
            if not text.strip():
                print("No text provided for synthesis")
                return False
                
            # Set up the synthesis input
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            # Build the voice request
            voice = texttospeech.VoiceSelectionParams(
                language_code=self.language_code,
                name=self.voice_name if self.voice_name else None,
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )
            
            # Select the type of audio file
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            
            # Perform the text-to-speech request
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Write the response to the output file
            with open(output_file_path, "wb") as out:
                out.write(response.audio_content)
                
            print(f"Audio content written to file: {output_file_path}")
            return True
            
        except Exception as e:
            print(f"Error during text-to-speech synthesis: {e}")
            return False
    
    def get_audio_content(self, text: str) -> Optional[bytes]:
        """
        Convert text to speech and return audio content as bytes
        
        Args:
            text: Text to convert to speech
            
        Returns:
            Audio content as bytes or None if synthesis failed
        """
        try:
            if not text.strip():
                return None
                
            # Set up the synthesis input
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            # Build the voice request
            voice = texttospeech.VoiceSelectionParams(
                language_code=self.language_code,
                name=self.voice_name if self.voice_name else None,
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )
            
            # Select the type of audio file
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            
            # Perform the text-to-speech request
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            return response.audio_content
            
        except Exception as e:
            print(f"Error during text-to-speech synthesis: {e}")
            return None
    
    def list_voices(self) -> list:
        """
        List available voices for the current language
        
        Returns:
            List of available voice names
        """
        try:
            voices = self.client.list_voices()
            
            # Filter voices by language code
            available_voices = []
            for voice in voices.voices:
                if self.language_code in voice.language_codes:
                    available_voices.append(voice.name)
                    
            return available_voices
            
        except Exception as e:
            print(f"Error listing voices: {e}")
            return []