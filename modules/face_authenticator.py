import cv2
import time

class FaceAuthenticator:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def detect_face(self, timeout=5, debug=True, debug_duration=2) -> bool:
        """
        Detects a face using OpenCV's Haar cascades within a timeout window.
        Always shows webcam preview if debug=True.
        """
        start_time = time.time()
        print("Face detection started. Waiting for user...")

        while time.time() - start_time < timeout:
            ret, frame = self.cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60)
            )

            if debug:
                # Draw rectangles on detected faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                cv2.imshow("Face Detection", frame)
                if cv2.waitKey(5) & 0xFF == 27:  # ESC to exit early
                    break

            if len(faces) > 0:
                return True

        if debug:
            cv2.destroyAllWindows()
        return False

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
