"""
Speech-to-Text service using Google Cloud Speech API
"""
import io
from google.cloud import speech
from typing import Optional


class SpeechToTextService:
    """Service for converting speech to text using Google Cloud Speech API"""
    
    def __init__(self, language_code: str = "en-US"):
        """
        Initialize the Speech-to-Text service
        
        Args:
            language_code: Language code for speech recognition (e.g., "en-US", "es-ES")
        """
        self.client = speech.SpeechClient()
        self.language_code = language_code
    
    def transcribe_audio_file(self, audio_file_path: str) -> Optional[str]:
        """
        Transcribe audio from a file
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Transcribed text or None if transcription failed
        """
        try:
            with io.open(audio_file_path, "rb") as audio_file:
                content = audio_file.read()
                
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code=self.language_code,
            )
            
            response = self.client.recognize(config=config, audio=audio)
            
            # Combine all results
            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript
                
            return transcript if transcript else None
            
        except Exception as e:
            print(f"Error during transcription: {e}")
            return None
    
    def transcribe_audio_content(self, audio_content: bytes) -> Optional[str]:
        """
        Transcribe audio from raw bytes
        
        Args:
            audio_content: Raw audio bytes
            
        Returns:
            Transcribed text or None if transcription failed
        """
        try:
            audio = speech.RecognitionAudio(content=audio_content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code=self.language_code,
            )
            
            response = self.client.recognize(config=config, audio=audio)
            
            # Combine all results
            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript
                
            return transcript if transcript else None
            
        except Exception as e:
            print(f"Error during transcription: {e}")
            return None