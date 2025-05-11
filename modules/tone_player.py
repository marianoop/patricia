import numpy as np
import sounddevice as sd

"""
A class for generating and playing valid and error sounds using Sounddevice.
"""
class TonePlayer:

    def __init__(self, sample_rate=44100.0, duration=0.25, base_frequency=220.0):
        self.sample_rate = sample_rate # Sampling frequency (it must be a floating point number)
        self.duration = duration # The default duration of generated sounds in seconds
        self.base_frequency = base_frequency # base frequency (Hz)

    def play_valid_tone(self):
        harmonic_interval = 3/2
        fifth_above = self._get_interval(harmonic_interval)
        sound = self._gen_sine_with_sidebands(1.0, 1.0, self.base_frequency, fifth_above)
        self._play_sound(sound)

    def play_error_tone(self):
        inharmonic_interval = 8/5
        minor_six_above = self._get_interval(inharmonic_interval) # Inharmonic interval
        sound = self._gen_sine_with_sidebands(1.0, 1.0, self.base_frequency, minor_six_above)
        self._play_sound(sound)

    def _gen_sine(self, amplitude, frequency):
        nd_array = np.arange(self.sample_rate * self.duration)  # N dimensional array of samples
        sampling_interval = 1 / self.sample_rate  # Sampling interval equals 1 over sampling frequency
        y = (amplitude * np.sin(2 * np.pi * frequency * nd_array * sampling_interval)).astype(np.float32)
        return y

    def _gen_sine_with_sidebands(self, amplitudeA, amplitudeB, frequency1, frequency2):
        # Generate base signals
        y1 = self._gen_sine(amplitudeA, frequency1)  # Signal 1: frequency 1
        y2 = self._gen_sine(amplitudeB, frequency2)  # Signal 2: frequency 1

        # Superimpose: add y1 to y2 to obtain a superimposed signal consisting of two individual frequencies
        y3 = y1 + y2

        # Intermodulate: multiply y1 by y2 to obtain the sum and the difference of their frequencies
        y4 = y1 * y2 * 0.5  # Reduce the amplitude of intermodulated components by half

        # Add sidebands: add y4 to y3 to increase dissonance or create distortion (except when y1 | y2)
        y5 = y3 + y4

        # Normalize to prevent clipping
        y5 = np.clip(y5, -1.0, 1.0)

        return y5

    def _get_interval(self, frequency_multiplier):
        return self.base_frequency * frequency_multiplier

    def _play_sound(self, sound):
        sd.play(sound)
        sd.wait()
        sd.stop()