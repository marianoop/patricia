import cv2
import time

"""
A class for detecting human faces in real time using a webcam.
"""
class FaceDetector:
    def __init__(self, max_attempts=3, preview=False, delay_seconds=5.0):
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
                    continue  # Skip if frame could not be read

                found, faces = self._detect_face(frame)

                if self.preview:
                    self._show_preview(frame, faces)
                    time.sleep(self.delay_seconds)

                if found:
                    print("✅ Face detected")
                    # Clean up the preview if it was enabled
                    if self.preview:
                        cv2.destroyAllWindows()
                    yield True, False
                    return

                # Calculate remaining attempts
                remaining_attempts = self.max_attempts - attempt - 1
                if remaining_attempts > 0:
                    print(f"❌ No face detected. {remaining_attempts} attempt(s) left")
                    yield False, False
                else:
                    print("❌ No face detected. No attempts left")
                    yield False, True
                    return

                time.sleep(self.delay_seconds)

        finally:
            self._close_camera()

    def _open_camera(self): # Open the webcam for capturing video frames
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise RuntimeError("[Face Detector] Error opening webcam.")

    def _close_camera(self): # Release the camera resource and destroys any open OpenCV windows
        if self.camera:
            self.camera.release()
            cv2.destroyAllWindows()  #

    def _detect_face(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale( gray, scaleFactor=1.3, minNeighbors=5)
        return len(faces) > 0, faces

    def _show_preview(self, frame, faces):
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("Face Preview", frame)

        # Add a small delay for the preview, clear only this specific window if no face is detected
        cv2.waitKey(500)
        cv2.destroyWindow("Face Preview")