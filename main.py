"""
Main application orchestrating Speech-to-Text, Translation, and Text-to-Speech services
"""
import os
import sys
from datetime import datetime
from speech_to_text import SpeechToTextService
from translation import TranslationService
from text_to_speech import TextToSpeechService


class SpeechTranslationPipeline:
    """Main pipeline that orchestrates STT -> Translation -> TTS"""
    
    def __init__(self, source_language: str = "en-US", target_language: str = "es"):
        """
        Initialize the speech translation pipeline
        
        Args:
            source_language: Source language code for speech recognition
            target_language: Target language code for translation and synthesis
        """
        self.source_language = source_language
        self.target_language = target_language
        
        # Initialize services
        self.stt_service = SpeechToTextService(language_code=source_language)
        self.translation_service = TranslationService()
        
        # Map language codes for TTS (remove region codes if present)
        tts_language = target_language
        if len(target_language) == 2:
            # Add default region for TTS
            language_mapping = {
                'es': 'es-ES',
                'fr': 'fr-FR',
                'de': 'de-DE',
                'it': 'it-IT',
                'pt': 'pt-PT',
                'ja': 'ja-JP',
                'ko': 'ko-KR',
                'zh': 'zh-CN',
                'en': 'en-US'
            }
            tts_language = language_mapping.get(target_language, f"{target_language}-{target_language.upper()}")
            
        self.tts_service = TextToSpeechService(language_code=tts_language)
    
    def process_audio_file(self, input_audio_path: str, output_audio_path: str = None) -> dict:
        """
        Process an audio file through the complete pipeline
        
        Args:
            input_audio_path: Path to input audio file
            output_audio_path: Path for output audio file (optional)
            
        Returns:
            Dictionary with processing results
        """
        results = {
            'success': False,
            'original_text': None,
            'translated_text': None,
            'output_audio_path': None,
            'error': None
        }
        
        try:
            # Step 1: Speech-to-Text
            print("Step 1: Converting speech to text...")
            original_text = self.stt_service.transcribe_audio_file(input_audio_path)
            
            if not original_text:
                results['error'] = "Failed to transcribe audio"
                return results
                
            results['original_text'] = original_text
            print(f"Transcribed text: {original_text}")
            
            # Step 2: Translation
            print("Step 2: Translating text...")
            translated_text = self.translation_service.translate_text(
                original_text, 
                self.target_language, 
                self.source_language.split('-')[0]  # Remove region code for translation
            )
            
            if not translated_text:
                results['error'] = "Failed to translate text"
                return results
                
            results['translated_text'] = translated_text
            print(f"Translated text: {translated_text}")
            
            # Step 3: Text-to-Speech
            print("Step 3: Converting translated text to speech...")
            if not output_audio_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_audio_path = f"output_{timestamp}.mp3"
                
            success = self.tts_service.synthesize_text(translated_text, output_audio_path)
            
            if not success:
                results['error'] = "Failed to synthesize speech"
                return results
                
            results['output_audio_path'] = output_audio_path
            results['success'] = True
            
            print(f"Pipeline completed successfully! Output saved to: {output_audio_path}")
            return results
            
        except Exception as e:
            results['error'] = f"Pipeline error: {e}"
            print(f"Error in pipeline: {e}")
            return results
    
    def process_audio_content(self, audio_content: bytes, output_audio_path: str = None) -> dict:
        """
        Process raw audio content through the complete pipeline
        
        Args:
            audio_content: Raw audio bytes
            output_audio_path: Path for output audio file (optional)
            
        Returns:
            Dictionary with processing results
        """
        results = {
            'success': False,
            'original_text': None,
            'translated_text': None,
            'output_audio_path': None,
            'error': None
        }
        
        try:
            # Step 1: Speech-to-Text
            print("Step 1: Converting speech to text...")
            original_text = self.stt_service.transcribe_audio_content(audio_content)
            
            if not original_text:
                results['error'] = "Failed to transcribe audio"
                return results
                
            results['original_text'] = original_text
            print(f"Transcribed text: {original_text}")
            
            # Step 2: Translation
            print("Step 2: Translating text...")
            translated_text = self.translation_service.translate_text(
                original_text, 
                self.target_language, 
                self.source_language.split('-')[0]  # Remove region code for translation
            )
            
            if not translated_text:
                results['error'] = "Failed to translate text"
                return results
                
            results['translated_text'] = translated_text
            print(f"Translated text: {translated_text}")
            
            # Step 3: Text-to-Speech
            print("Step 3: Converting translated text to speech...")
            if not output_audio_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_audio_path = f"output_{timestamp}.mp3"
                
            success = self.tts_service.synthesize_text(translated_text, output_audio_path)
            
            if not success:
                results['error'] = "Failed to synthesize speech"
                return results
                
            results['output_audio_path'] = output_audio_path
            results['success'] = True
            
            print(f"Pipeline completed successfully! Output saved to: {output_audio_path}")
            return results
            
        except Exception as e:
            results['error'] = f"Pipeline error: {e}"
            print(f"Error in pipeline: {e}")
            return results


def main():
    """Main function to demonstrate the speech translation pipeline"""
    print("GCP Speech Translation Pipeline Demo")
    print("=====================================")
    
    # Check for GCP credentials
    if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        print("Please set it to point to your GCP service account key file.")
        print("Example: export GOOGLE_APPLICATION_CREDENTIALS='/path/to/your/keyfile.json'")
        return
    
    # Configuration
    source_language = "en-US"  # English (US)
    target_language = "es"     # Spanish
    
    print(f"Source language: {source_language}")
    print(f"Target language: {target_language}")
    print()
    
    # Initialize pipeline
    pipeline = SpeechTranslationPipeline(source_language, target_language)
    
    # Check for input audio file
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found.")
            return
            
        print(f"Processing audio file: {input_file}")
        results = pipeline.process_audio_file(input_file)
        
        if results['success']:
            print("\n✅ Pipeline completed successfully!")
            print(f"Original text: {results['original_text']}")
            print(f"Translated text: {results['translated_text']}")
            print(f"Output audio: {results['output_audio_path']}")
        else:
            print(f"\n❌ Pipeline failed: {results['error']}")
    else:
        print("Usage: python main.py <input_audio_file>")
        print("Example: python main.py sample_audio.wav")
        print("\nNote: Input audio should be 16kHz mono WAV format for best results.")


if __name__ == "__main__":
    main()