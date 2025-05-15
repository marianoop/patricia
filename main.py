import sys

from modules.soundtrack_player import SoundtrackPlayer
from modules.face_detector import FaceDetector
from modules.audio_prompter import AudioPlayer
from modules.birthdate_validator import BirthdateValidator
from modules.swipe_detector import SwipeDetector


def main():
    # Setup
    face_detector = FaceDetector() # Pass preview=True by argument if debbuging is needed
    soundtrack_player = SoundtrackPlayer()
    validator = BirthdateValidator()
    swipe_detector = SwipeDetector(preview=True) # Pass preview=True by argument if debbuging is needed
    audio_player = AudioPlayer()

    # Step 1: Face Detection
    print("[Patricia] Please position yourself in front of the camera...")

    for result, is_last_attempt in face_detector.detect():
        if result:
            audio_player.play("1-Welcome.wav")
            soundtrack_player.play("Soundtrack1.wav")
            break
        else:
            audio_player.play("3-Access denied.wav")
            if is_last_attempt:
                sys.exit("⛔ ACCESS PERMANENTLY DENIED ⛔")

    # Step 2: Ask for Birthdate
    audio_player.play("2-Enter birthdate.wav")
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
    try:
        for attempt in range(swipe_detector.max_attempts):
            success = swipe_detector.detect_swipe()

            if success:
                print("✅ Protocol activated")
                audio_player.play("6-Initiating power outage.wav")
                break

            else:
                if attempt < swipe_detector.max_attempts - 1:
                    audio_player.play("7-Follow the instructions.wav")  # Only if not the last attempt

        else:
            audio_player.play("8-Follow the, initiating power outage.wav")

    finally:
        print("Step 4: Access granted")

if __name__ == "__main__":
    main()
