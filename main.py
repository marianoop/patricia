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
    swipe_detector = SwipeDetector() # Pass preview=True by argument if debbuging is needed
    prompter = AudioPlayer()

    # Step 1: Face Detection
    print("Please position yourself in front of the camera...")
    if face_detector.detect():
        state.face_detected = True
        prompter.play_and_speak("Access granted. Welcome Participant", "welcome.mp3") # Send welcome message
    else:
        print("Access denied")
        return

    # Step 2: Ask for Birthdate
    prompter.play_and_speak("Please enter your birthdate (dd/mm/yyyy):", "validate.mp3")
    while True:
        birthdate = input("Please, enter your birthdate (DD/MM/YYYY): ")
        print(f"You entered: {birthdate}")
        if validator.validate(birthdate):
            break

    # Step 3: Swipe Detection
    prompter.play_and_speak("Swipe your hand if you want to start massive shutdown", "validate.mp3")
    if swipe_detector.detect_swipe():
        print("✅ Swipe detected!")
    else:
        print("❌ No swipe detected.")

if __name__ == "__main__":
    main()
