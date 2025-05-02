import cv2
from collections import deque
import time
import math

"""
A  cass for detecting left-to-right hand swipes.
"""
class SwipeDetector:
    def __init__(self, validation_time=30.0, min_displacement=800):
        self.validation_time = validation_time
        self.min_displacement = min_displacement
        self.position_history = deque()
        self.y_position_history = deque()

    def detect_swipe(self):
        cap = cv2.VideoCapture(0)
        ret, prev_frame = cap.read()
        if not ret:
            print("❌ Failed to read webcam.")
            return False

        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        start_time = time.time()

        try:
            while True:
                if time.time() - start_time > self.validation_time:
                    return False

                ret, frame = cap.read()
                if not ret:
                    continue

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                diff = cv2.absdiff(prev_gray, gray)
                blurred = cv2.GaussianBlur(diff, (5, 5), 0)
                _, thresh = cv2.threshold(blurred, 25, 255, cv2.THRESH_BINARY)
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    if area < 5000:
                        continue

                    hull = cv2.convexHull(cnt)
                    hull_area = cv2.contourArea(hull)
                    if hull_area == 0:
                        continue
                    solidity = float(area) / hull_area

                    x, y, w, h = cv2.boundingRect(cnt)
                    aspect_ratio = w / float(h)

                    perimeter = cv2.arcLength(cnt, True)
                    circularity = (4 * math.pi * area) / (perimeter * perimeter) if perimeter else 0

                    is_likely_hand = (
                            0.3 < solidity < 0.9 and
                            0.5 < aspect_ratio < 1.5 and
                            circularity < 0.6
                    )

                    if not is_likely_hand:
                        continue

                    cx = x + w // 2
                    cy = y + h // 2
                    self.position_history.append(cx)
                    self.y_position_history.append(cy)

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                if len(self.position_history) >= 5:
                    dx = self.position_history[0] - self.position_history[-1]
                    dy = abs(self.y_position_history[0] - self.y_position_history[-1])

                    if dx > self.min_displacement and dy < self.min_displacement * 0.5:
                        return True
                    elif dx < -self.min_displacement or dy > self.min_displacement * 0.5:
                        self.position_history.clear()
                        self.y_position_history.clear()

                prev_gray = gray.copy()
                cv2.imshow("Hand Swipe Detection", frame)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()
