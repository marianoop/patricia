import sys
import time

from modules.soundtrack_player import SoundtrackPlayer
from modules.face_detector import FaceDetector
from modules.audio_prompter import AudioPlayer
from modules.birthdate_validator import BirthdateValidator
from modules.swipe_detector import SwipeDetector

def main():
    # Initial Setup
    face_detector = FaceDetector() # add parameter (preview=True) if debbuging is needed
    soundtrack_player = SoundtrackPlayer()
    validator = BirthdateValidator()
    swipe_detector = SwipeDetector(preview=True)
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
    success = False
    try:
        for attempt in range(swipe_detector.max_attempts):
            success = swipe_detector.detect_swipe()

            if success:
                print("✅ Protocol activated")
                audio_player.play("6-Initiating power outage.wav")
                break

            else:
                if attempt < swipe_detector.max_attempts - 1:
                    audio_player.play("7-Follow the instructions.wav")

    finally:
        if not success:
            print("✅ Protocol activated")
            audio_player.play("8-Follow the, initiating power outage.wav")

    # Step 4: Grant Access
    soundtrack_player.stop()
    soundtrack_player.play("Soundtrack5.wav")

    seconds_to_incoming_call = 2
    seconds_to_ask_request = 25

    time.sleep(seconds_to_incoming_call)
    print("[Patricia] Incoming call...")

    time.sleep(seconds_to_ask_request)

    while True:
        user_response = input("[Patricia] Grant access? (Y/N): ").strip()

        if user_response.upper() in ["Y", "N"]:
            break
        else:
            print("❌ Invalid input")

    soundtrack_player.stop()
    audio_player.play("9-Warning.wav")

    if user_response.upper() == "Y":
        soundtrack_player.play_and_wait("Soundtrack6Y.wav")
    else:
        soundtrack_player.play_and_wait("Soundtrack6N.wav")

    # Step 5: Thank you
    audio_player.play("10-Thank you.wav")
    audio_player.play("Farewell song.wav")

if __name__ == "__main__":
    main()
