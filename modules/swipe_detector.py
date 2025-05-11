import cv2
from collections import deque
import time
import math

"""
A  class for detecting left-to-right hand swipes.
"""
class SwipeDetector:
    def __init__(self, preview=False, validation_time=5.0, max_attempts=3, min_displacement=700, min_countour_area=10000):
        self.preview = preview  # Show webcam preview with bounding boxes
        self.validation_time = validation_time  # Time limit per swipe attempt
        self.max_attempts = max_attempts  # Max swipe attempts allowed
        self.min_displacement = min_displacement  # Required horizontal movement
        self.min_countour_area = min_countour_area  # Minimum contour area to consider
        self.position_history = deque()  # Track x positions of movement
        self.y_position_history = deque()  # Track y positions for vertical consistency

    def _process_contours(self, contours):
        for cnt in contours:  # Calculate contour area and ignore small contours
            area = cv2.contourArea(cnt)
            if area < self.min_countour_area:
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

            # Determine if the contour likely represents a hand
            is_likely_hand = (
                0.3 < solidity < 0.9 and
                0.5 < aspect_ratio < 1.5 and
                circularity < 0.6
            )

            if is_likely_hand:
                # Update position history
                cx = x + w // 2
                cy = y + h // 2
                self.position_history.append(cx)
                self.y_position_history.append(cy)
                return (x, y, w, h)

        return None

    def _check_swipe(self):  # Validates whether the detected motion represents a valid left-to-right hand swipe
        if len(self.position_history) >= 5:
            dx = self.position_history[0] - self.position_history[-1]
            dy = abs(self.y_position_history[0] - self.y_position_history[-1])

            if dx > self.min_displacement and dy < self.min_displacement * 0.5:
                return True
            elif dx < -self.min_displacement or dy > self.min_displacement * 0.5:
                self._reset_position_history()  # Invalid motion, reset history

        return False

    def _reset_position_history(self):  # Clears position history to reset the state after invalid motion
        self.position_history.clear()
        self.y_position_history.clear()

    def _draw_bounding_box(self, frame, bbox):
        """
        Draws a bounding box around the detected hand (only if self.preview is True).
        :param frame: Current video frame.
        :param bbox: Tuple (x, y, w, h) representing the bounding box.
        """
        if bbox and self.preview:
            x, y, w, h = bbox
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    def detect_swipe(self):  # Main method to detect left-to-right hand swipes in the webcam feed.
        cap = cv2.VideoCapture(0)
        ret, prev_frame = cap.read()
        if not ret:
            print("[Swipe Detector] Failed to read webcam.")
            return False

        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        start_time = time.time()

        try:
            while True:
                # Check elapsed time to stop detection
                if time.time() - start_time > self.validation_time:
                    return False  # Time limit reached, no valid swipe

                ret, frame = cap.read()
                if not ret:
                    continue

                # Frame processing
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                diff = cv2.absdiff(prev_gray, gray)
                blurred = cv2.GaussianBlur(diff, (5, 5), 0)
                _, thresh = cv2.threshold(blurred, 25, 255, cv2.THRESH_BINARY)
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Process contours and update position history
                bbox = self._process_contours(contours)

                # Draw bounding box if enabled
                self._draw_bounding_box(frame, bbox)

                # Check if a swipe was detected
                if self._check_swipe():
                    return True

                # Update previous frame
                prev_gray = gray.copy()

                # Show the preview if enabled
                if self.preview:
                    cv2.imshow("Hand Swipe Detection", frame)
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break

        finally:
            cap.release()
            if self.preview:
                cv2.destroyAllWindows()
                cv2.waitKey(1)
                time.sleep(0.1)
