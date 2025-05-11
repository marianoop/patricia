import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

"""
A class for playing background music using pygame.mixer. 
"""
class SoundtrackPlayer:

    def __init__(self, base_path="resources/audio/"):
        self.base_path = base_path
        pygame.mixer.init()

    def play(self, filename: str, loops=-1):  # -1 will loop forever
        try:
            file_path = os.path.join(self.base_path, filename)
            self.stop()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play(loops=loops, fade_ms=-1)

            return True

        except Exception as e:
            print(f"[SoundtrackPlayer] Error playing sound in loop: {e}")
            return False

    def stop(self):  # Stop any currently playing looping soundtrack
        pygame.mixer.music.stop()
