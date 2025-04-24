from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pygame
import os

class BirthdateValidator:
    DTMF_FREQS = {
        '1': 1209,
        '2': 1336,
        '3': 1477,
        '4': 1209,
        '5': 1336,
        '6': 1477,
        '7': 1209,
        '8': 1336,
        '9': 1477,
        '0': 1336
    }

    def __init__(self, audio_dir="audio/errors/"):
        self.audio_dir = audio_dir
        pygame.mixer.init()

    def play_error_sound(self):
        error_file = os.path.join(self.audio_dir, "error.wav")
        if os.path.exists(error_file):
            pygame.mixer.music.load(error_file)
            pygame.mixer.music.play()

    def play_dtmf_tone(self, digit: str, duration=0.5):
        if digit not in self.DTMF_FREQS:
            self.play_error_sound()
            return

        fs = 44100  # Sampling rate
        t = np.linspace(0, duration, int(fs * duration), endpoint=False)
        freq = self.DTMF_FREQS[digit]
        wave = np.sin(2 * np.pi * freq * t)

        plt.plot(t, wave)
        plt.title(f"DTMF Tone: {digit}")
        plt.show()

    def validate_birthdate(self, birthdate_str: str) -> str:
        try:
            parsed = datetime.strptime(birthdate_str, "%d/%m/%Y")
        except ValueError:
            return "denied_non_numeric"

        threshold = datetime.strptime("01/01/2032", "%d/%m/%Y")
        if parsed > threshold:
            return "denied_adult"
        return "granted"
