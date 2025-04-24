import os
import sounddevice as sd
import soundfile as sf

"""
A class to manage audio prompts and playback using Sounddevice.
"""
class AudioPrompter:

    def __init__(self, audio_dir="resources/audio/"):
        self.audio_dir = audio_dir

    def play(self, filename):
        path = os.path.join(self.audio_dir, filename) # Construct the full file path

        if not os.path.exists(path): # Check if the audio file exists
            print(f"[AudioPrompter] File not found: {path}")
            return False

        try:
            data, samplerate = sf.read(path) # Load the audio data and sample rate

            sd.play(data, samplerate) # Play the audio
            sd.wait()  # Wait for the playback to complete

            return True

        except Exception as e:
            print(f"[AudioPrompter] Error playing file {filename}: {e}")
            return False

    def speak(self, message, audio_file):
        print(f"[Patricia] {message}")
        success = self.play(audio_file)
        if not success:
            print("[AudioPrompter] Failed to play audio.")