"""
Translation service using Google Cloud Translate API
"""
from google.cloud import translate_v2 as translate
from typing import Optional


class TranslationService:
    """Service for translating text using Google Cloud Translate API"""
    
    def __init__(self):
        """Initialize the Translation service"""
        self.client = translate.Client()
    
    def translate_text(self, text: str, target_language: str, source_language: str = None) -> Optional[str]:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_language: Target language code (e.g., "es", "fr", "de")
            source_language: Source language code (optional, auto-detected if None)
            
        Returns:
            Translated text or None if translation failed
        """
        try:
            if not text.strip():
                return None
                
            result = self.client.translate(
                text,
                target_language=target_language,
                source_language=source_language
            )
            
            return result['translatedText']
            
        except Exception as e:
            print(f"Error during translation: {e}")
            return None
    
    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect the language of the given text
        
        Args:
            text: Text to analyze
            
        Returns:
            Language code or None if detection failed
        """
        try:
            if not text.strip():
                return None
                
            result = self.client.detect_language(text)
            return result['language']
            
        except Exception as e:
            print(f"Error during language detection: {e}")
            return None
    
    def get_supported_languages(self) -> list:
        """
        Get list of supported languages
        
        Returns:
            List of supported language codes
        """
        try:
            results = self.client.get_languages()
            return [result['language'] for result in results]
            
        except Exception as e:
            print(f"Error getting supported languages: {e}")
            return []