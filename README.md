# GCP Speech Integration Sample

This sample demonstrates a complete speech processing pipeline using Google Cloud Platform services:

1. **Speech-to-Text**: Converts voice input to text using GCP Speech API
2. **Translation**: Translates the transcribed text to a desired language using GCP Translate API  
3. **Text-to-Speech**: Converts the translated text back to audio using GCP Text-to-Speech API

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up GCP authentication:
   - Create a GCP project and enable Speech, Translate, and Text-to-Speech APIs
   - Create a service account and download the JSON key file
   - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your key file

3. Run the sample:
```bash
python main.py
```

## Usage

The application will:
1. Record audio from your microphone
2. Transcribe the audio to text
3. Translate the text to your target language
4. Convert the translated text to speech
5. Save the output audio file

## Configuration

You can modify the source and target languages in the configuration section of `main.py`. 
