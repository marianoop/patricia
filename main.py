from modules.soundtrack_player import SoundtrackPlayer
from modules.state_manager import StateManager
from modules.face_detector import FaceDetector
from modules.audio_prompter import AudioPlayer
from modules.birthdate_validator import BirthdateValidator
from modules.swipe_detector import SwipeDetector


def main():
    # Setup
    state = StateManager()
    face_detector = FaceDetector() # Pass preview=True by argument if debbuging is needed
    soundtrack_player = SoundtrackPlayer()
    validator = BirthdateValidator()
    swipe_detector = SwipeDetector(preview=True) # Pass preview=True by argument if debbuging is needed
    audio_player = AudioPlayer()

    # Step 1: Face Detection
    print("[Patricia] Please position yourself in front of the camera...")
    if face_detector.detect():
        audio_player.play("1-Welcome.wav")
        soundtrack_player.play("Soundtrack1.wav")
        state.face_detected = True
    else:
        print("Access denied")
        return

    # Step 2: Ask for Birthdate
    while True:
        birthdate = input("[Patricia] Please, enter your birthdate (DD/MM/YYYY): ")
        if validator.validate(birthdate):
            soundtrack_player.stop()
            audio_player.play("4-Access granted.wav")
            soundtrack_player.play("Soundtrack4.wav")
            break
        else:
            audio_player.play("3-Access denied.wav")

    # Step 3: Swipe Detection
    audio_player.play("5-Swipe hand.wav")
    if swipe_detector.detect_swipe():
        print("✅ Protocol activated")
    else:
        print("❌ No swipe detected.")

if __name__ == "__main__":
    main()
