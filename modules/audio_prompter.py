import os
import pygame

class AudioPrompter:
    def __init__(self, audio_dir="audio/"):
        self.audio_dir = audio_dir
        pygame.mixer.init()

    def play(self, filename: str):
        """Play an audio file from the audio directory."""
        path = os.path.join(self.audio_dir, filename)
        if not os.path.exists(path):
            print(f"[AudioPrompter] File not found: {path}")
            return
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

    def speak(self, message: str, audio_file: str):
        """Print the message and play the corresponding audio."""
        print(f"[Patricia] {message}")
        self.play(audio_file)