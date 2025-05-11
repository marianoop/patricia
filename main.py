from modules.state_manager import StateManager
from modules.face_detector import FaceDetector
from modules.audio_prompter import AudioPlayer
from modules.birthdate_validator import BirthdateValidator
from modules.swipe_detector import SwipeDetector


def main():
    # Setup
    state = StateManager()
    face_detector = FaceDetector() # Pass preview=True by argument if debbuging is needed
    validator = BirthdateValidator()
    swipe_detector = SwipeDetector(preview=True) # Pass preview=True by argument if debbuging is needed
    prompter = AudioPlayer()

    # Step 1: Face Detection
    print("[Patricia] Please position yourself in front of the camera...")
    if face_detector.detect():
        prompter.play("1-Welcome.wav")
        state.face_detected = True
    else:
        print("Access denied")
        return

    # Step 2: Ask for Birthdate
    while True:
        birthdate = input("[Patricia] Please, enter your birthdate (DD/MM/YYYY): ")
        # print(f"You entered: {birthdate}")
        if validator.validate(birthdate):
            prompter.play("4-Access granted.wav")
            break
        else:
            prompter.play("3-Access denied.wav")

    # Step 3: Swipe Detection
    prompter.play_and_speak("Swipe your hand if you want to start massive shutdown", "validate.mp3")
    if swipe_detector.detect_swipe():
        print("✅ Swipe detected!")
    else:
        print("❌ No swipe detected.")

if __name__ == "__main__":
    main()
