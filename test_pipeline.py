"""
Basic tests for the speech translation pipeline components
"""
import unittest
from unittest.mock import Mock, patch, mock_open
import os
import sys

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from speech_to_text import SpeechToTextService
from translation import TranslationService
from text_to_speech import TextToSpeechService
from main import SpeechTranslationPipeline


class TestSpeechToTextService(unittest.TestCase):
    """Test cases for Speech-to-Text service"""
    
    @patch('speech_to_text.speech.SpeechClient')
    def test_initialization(self, mock_client):
        """Test service initialization"""
        service = SpeechToTextService("en-US")
        self.assertEqual(service.language_code, "en-US")
        mock_client.assert_called_once()
    
    @patch('speech_to_text.speech.SpeechClient')
    @patch('builtins.open', new_callable=mock_open, read_data=b'fake_audio_data')
    def test_transcribe_audio_file(self, mock_file, mock_client):
        """Test audio file transcription"""
        # Mock the speech client response
        mock_result = Mock()
        mock_result.alternatives = [Mock()]
        mock_result.alternatives[0].transcript = "Hello world"
        
        mock_response = Mock()
        mock_response.results = [mock_result]
        
        mock_client_instance = Mock()
        mock_client_instance.recognize.return_value = mock_response
        mock_client.return_value = mock_client_instance
        
        service = SpeechToTextService()
        result = service.transcribe_audio_file("test.wav")
        
        self.assertEqual(result, "Hello world")
        mock_file.assert_called_once_with("test.wav", "rb")


class TestTranslationService(unittest.TestCase):
    """Test cases for Translation service"""
    
    @patch('translation.translate.Client')
    def test_initialization(self, mock_client):
        """Test service initialization"""
        service = TranslationService()
        mock_client.assert_called_once()
    
    @patch('translation.translate.Client')
    def test_translate_text(self, mock_client):
        """Test text translation"""
        mock_client_instance = Mock()
        mock_client_instance.translate.return_value = {
            'translatedText': 'Hola mundo'
        }
        mock_client.return_value = mock_client_instance
        
        service = TranslationService()
        result = service.translate_text("Hello world", "es")
        
        self.assertEqual(result, "Hola mundo")
    
    @patch('translation.translate.Client')
    def test_detect_language(self, mock_client):
        """Test language detection"""
        mock_client_instance = Mock()
        mock_client_instance.detect_language.return_value = {
            'language': 'en'
        }
        mock_client.return_value = mock_client_instance
        
        service = TranslationService()
        result = service.detect_language("Hello world")
        
        self.assertEqual(result, "en")


class TestTextToSpeechService(unittest.TestCase):
    """Test cases for Text-to-Speech service"""
    
    @patch('text_to_speech.texttospeech.TextToSpeechClient')
    def test_initialization(self, mock_client):
        """Test service initialization"""
        service = TextToSpeechService("en-US")
        self.assertEqual(service.language_code, "en-US")
        mock_client.assert_called_once()
    
    @patch('text_to_speech.texttospeech.TextToSpeechClient')
    @patch('builtins.open', new_callable=mock_open)
    def test_synthesize_text(self, mock_file, mock_client):
        """Test text synthesis"""
        mock_response = Mock()
        mock_response.audio_content = b'fake_audio_content'
        
        mock_client_instance = Mock()
        mock_client_instance.synthesize_speech.return_value = mock_response
        mock_client.return_value = mock_client_instance
        
        service = TextToSpeechService()
        result = service.synthesize_text("Hello world", "output.mp3")
        
        self.assertTrue(result)
        mock_file.assert_called_once_with("output.mp3", "wb")


class TestSpeechTranslationPipeline(unittest.TestCase):
    """Test cases for the main pipeline"""
    
    def test_initialization(self):
        """Test pipeline initialization"""
        with patch('main.SpeechToTextService'), \
             patch('main.TranslationService'), \
             patch('main.TextToSpeechService'):
            pipeline = SpeechTranslationPipeline("en-US", "es")
            self.assertEqual(pipeline.source_language, "en-US")
            self.assertEqual(pipeline.target_language, "es")
    
    def test_language_mapping(self):
        """Test language code mapping for TTS"""
        with patch('main.SpeechToTextService'), \
             patch('main.TranslationService'), \
             patch('main.TextToSpeechService') as mock_tts:
            
            # Test short language code gets mapped correctly
            pipeline = SpeechTranslationPipeline("en-US", "es")
            mock_tts.assert_called_with(language_code="es-ES")


if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)