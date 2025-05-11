import os
import sounddevice as sd
import soundfile as sf

"""
A class to manage audio prompts and playback using Sounddevice.
"""
class AudioPlayer:
    def __init__(self, base_path="resources/audio/"):
        self.base_path = base_path

    def play(self, filename):
        path = os.path.join(self.base_path, filename) # Construct the full file path

        if not os.path.exists(path): # Check if the audio file exists
            print(f"[AudioPlayer] File not found: {path}")
            return False

        try:
            data, samplerate = sf.read(path) # Load the audio data and sample rate

            sd.play(data, samplerate) # Play the audio
            sd.wait()  # Wait for the playback to complete

            return True

        except Exception as e:
            print(f"[AudioPlayer] Error playing file {filename}: {e}")
            return False