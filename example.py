"""
Example script demonstrating the speech translation pipeline
"""
import os
from main import SpeechTranslationPipeline


def run_example():
    """Run an example of the speech translation pipeline"""
    
    print("Speech Translation Pipeline Example")
    print("===================================")
    
    # Check for GCP credentials
    if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
        print("❌ Error: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        print("Please set it to point to your GCP service account key file.")
        print("Example: export GOOGLE_APPLICATION_CREDENTIALS='/path/to/your/keyfile.json'")
        return
    
    try:
        # Initialize pipeline: English -> Spanish
        print("Initializing pipeline (English -> Spanish)...")
        pipeline = SpeechTranslationPipeline(
            source_language="en-US", 
            target_language="es"
        )
        
        # Example 1: Process a sample audio file (if available)
        sample_files = ["sample.wav", "test.wav", "input.wav"]
        input_file = None
        
        for file in sample_files:
            if os.path.exists(file):
                input_file = file
                break
        
        if input_file:
            print(f"\n📁 Found sample audio file: {input_file}")
            print("Processing through pipeline...")
            
            results = pipeline.process_audio_file(input_file)
            
            if results['success']:
                print("✅ Pipeline completed successfully!")
                print(f"📝 Original text: {results['original_text']}")
                print(f"🌍 Translated text: {results['translated_text']}")
                print(f"🔊 Output audio: {results['output_audio_path']}")
            else:
                print(f"❌ Pipeline failed: {results['error']}")
        else:
            print("\n📁 No sample audio files found.")
            print("To test the pipeline, place a WAV audio file in the current directory.")
            print("Supported filenames: sample.wav, test.wav, input.wav")
            
        # Example 2: Show available configuration options
        print("\n⚙️  Configuration Examples:")
        print("English to French:")
        print('  pipeline = SpeechTranslationPipeline("en-US", "fr")')
        print("Spanish to English:")
        print('  pipeline = SpeechTranslationPipeline("es-ES", "en")')
        print("German to Italian:")
        print('  pipeline = SpeechTranslationPipeline("de-DE", "it")')
        
        # Example 3: Show supported languages
        print("\n🌍 Common language codes:")
        languages = {
            "en": "English",
            "es": "Spanish", 
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ja": "Japanese",
            "ko": "Korean",
            "zh": "Chinese"
        }
        
        for code, name in languages.items():
            print(f"  {code}: {name}")
            
    except Exception as e:
        print(f"❌ Error running example: {e}")
        print("Please ensure you have:")
        print("1. Installed dependencies: pip install -r requirements.txt")
        print("2. Set up GCP authentication")
        print("3. Enabled Speech, Translate, and Text-to-Speech APIs in your GCP project")


if __name__ == "__main__":
    run_example()