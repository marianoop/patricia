from modules.state_manager import StateManager
from modules.face_authenticator import FaceAuthenticator
from modules.audio_prompter import AudioPrompter
from modules.birthdate_validator import BirthdateValidator

def main():
    # Setup
    validator = BirthdateValidator()
    state = StateManager()
    face_auth = FaceAuthenticator()
    prompter = AudioPrompter(audio_dir="audio/")

    # Step 1: Face Detection
    # face_detected = face_auth.detect_face(timeout=10, debug=True, debug_duration=5)
    #
    # print("Please position yourself in front of the camera...")
    # if face_detected:
    #     state.face_detected = True
    #     prompter.speak("Welcome participant.", "welcome_participant.wav")
    # else:
    #     print("No face detected. Exiting.")
    #     face_auth.release()
    #     return



    # Step 3: Play DTMF tones or error sound
    # for char in birthdate:
    #     validator.play_dtmf_tone(char)

    # Step 2: Ask for Birthdate
    # prompter.speak("Please enter your birth date (rdd/mm/yyyy):", "please_enter_birthdate.wav")
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

    face_auth.release()

if __name__ == "__main__":
    main()
