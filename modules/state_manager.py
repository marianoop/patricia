class StateManager:
    def __init__(self):
        self.face_detected = False
        self.birthdate = None
        self.access_granted = False
        self.sound_detected = False
        self.protocol_started = False
        self.third_party_granted = None
        self.reminder_count = 0

    def reset(self):
        self.__init__()