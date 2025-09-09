# Sample Audio Files

To test the speech translation pipeline, you'll need audio files in WAV format. Here are some recommendations:

## Audio Format Requirements

- **Format**: WAV (recommended) or FLAC
- **Sample Rate**: 16kHz (recommended for best results)
- **Channels**: Mono (single channel)
- **Bit Depth**: 16-bit
- **Duration**: 10-60 seconds for testing

## Creating Test Audio

You can create test audio files using:

1. **Online tools**: Record using your browser's microphone
2. **Mobile apps**: Voice recorder apps (export as WAV if possible)
3. **Command line** (if you have ffmpeg):
   ```bash
   # Convert any audio file to the recommended format
   ffmpeg -i input.mp3 -ar 16000 -ac 1 -y sample.wav
   ```

## Sample Content Ideas

- **English**: "Hello, this is a test of the speech translation system."
- **Spanish**: "Hola, esta es una prueba del sistema de traducción de voz."
- **French**: "Bonjour, ceci est un test du système de traduction vocale."

## File Naming

Place your test audio files in the project directory with names like:
- `sample.wav`
- `test.wav` 
- `input.wav`

The example script will automatically detect and process these files.