import cv2
import time

"""
A class for detecting human faces in real time using a webcam.
"""
class FaceDetector:
    def __init__(self, max_attempts = 3, preview = False, delay_seconds= 1.0):
        self.max_attempts = max_attempts
        self.preview = preview
        self.delay_seconds = delay_seconds
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.camera = None

    def detect(self):
        self._open_camera()
        try:
            for attempt in range(self.max_attempts):
                ret, frame = self.camera.read()
                if not ret:
                    continue

                found, faces = self._detect_face(frame)

                if self.preview:
                    self._show_preview(frame, faces)
                    time.sleep(self.delay_seconds)

                if found:
                    print("✅ Face detected.")
                    return True

                print(f"❌ No face detected. Attempt {attempt + 1}/{self.max_attempts}")
                time.sleep(self.delay_seconds)
            return False
        finally:
            self._close_camera()

    def _open_camera(self):
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise RuntimeError("Could not open webcam.")

    def _close_camera(self):
        if self.camera:
            self.camera.release()
            cv2.destroyAllWindows()

    def _detect_face(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        return len(faces) > 0, faces

    def _show_preview(self, frame, faces):
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("Face Preview", frame)
        cv2.waitKey(500)  # Show for 500ms
        cv2.destroyWindow("Face Preview")