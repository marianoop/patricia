from modules.state_manager import StateManager
from modules.face_detector import FaceDetector
from modules.audio_prompter import AudioPlayer
from modules.birthdate_validator import BirthdateValidator

def main():

    # Setup
    state = StateManager()
    face_detector = FaceDetector(preview=False) # Pass preview=True by argument if debbuging is needed
    validator = BirthdateValidator()
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
    # prompter.speak("Please enter your birthdate (rdd/mm/yyyy):", "please_enter_birthdate.wav")
    while True:
        birthdate = input("Please, enter your birthdate (DD/MM/YYYY): ")
        print(f"You entered: {birthdate}")
        if validator.validate(birthdate):
            break


    # Step 4: Validate
    # result = validator.validate(birthdate)
    # if result == "granted":
    #     state.access_granted = True
    #     prompter.speak("Access Granted: Well Done", "access_granted_well_done.wav")
    # elif result == "denied_adult":
    #     prompter.speak("Access Denied: Adults Only", "access_denied_adults_only.wav")
    #     return
    # else:
    #     prompter.speak("Access Denied: Numbers Only", "access_denied_numbers_only.wav")
    #     return


if __name__ == "__main__":
    main()
