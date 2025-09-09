
import queue
import re
import sys

from google.cloud import speech

import pyaudio

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class MicrophoneStream:
    # ...existing code...
    def __init__(self: object, rate: int = RATE, chunk: int = CHUNK) -> None:
        # ...existing code...
        self._rate = rate
        self._chunk = chunk
        self._buff = queue.Queue()
        self.closed = True
    # ...existing code...
    def __enter__(self: object) -> object:
        # ...existing code...
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )
        self.closed = False
        return self
    # ...existing code...
    def __exit__(self: object, type: object, value: object, traceback: object) -> None:
        # ...existing code...
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()
    # ...existing code...
    def _fill_buffer(self: object, in_data: object, frame_count: int, time_info: object, status_flags: object) -> object:
        self._buff.put(in_data)
        return None, pyaudio.paContinue
    # ...existing code...
    def generator(self: object) -> object:
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b"".join(data)

# ...existing code...
def listen_print_loop(responses: object) -> str:
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue
        result = response.results[0]
        if not result.alternatives:
            continue
        transcript = result.alternatives[0].transcript
        overwrite_chars = " " * (num_chars_printed - len(transcript))
        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()
            num_chars_printed = len(transcript)
        else:
            print(transcript + overwrite_chars)
            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                print("Exiting..")
                break
            num_chars_printed = 0
    return transcript

# ...existing code...
