import cv2
import mediapipe as mp
from math import sqrt
import threading
import queue
import time

class BlinkDetectionThread(threading.Thread):
    def __init__(self, blink_queue):
        super().__init__()
        self.blink_queue = blink_queue
        self.stop_thread = False

        # Adjusted thresholds based on observed ratios
        self.HIGH_THRESHOLD = 4.1
        self.LOW_THRESHOLD = 3.1
        self.COOLDOWN_PERIOD = 1.0  # Cooldown period in seconds for single blinks

        # Blink state
        self.eyes_closed = False
        self.last_blink_time = 0
        self.last_single_blink_time = 0  # Tracks last single blink time

        # Mediapipe initialization
        self.LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        self.RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.7,
        )
        self.video_capture = cv2.VideoCapture(0)

    def landmarksDetection(self, image, results):
        image_height, image_width = image.shape[:2]
        mesh_coordinates = [
            (int(point.x * image_width), int(point.y * image_height))
            for point in results.multi_face_landmarks[0].landmark
        ]
        return mesh_coordinates

    def drawLandmarks(self, image, landmarks):
        for point in landmarks:
            cv2.circle(image, point, 2, (0, 255, 0), -1)
        return image

    def euclideanDistance(self, point, point1):
        x, y = point
        x1, y1 = point1
        return sqrt((x1 - x)**2 + (y1 - y)**2)

    def blinkRatio(self, landmarks):
        right_eye_landmark1 = landmarks[self.RIGHT_EYE[0]]
        right_eye_landmark2 = landmarks[self.RIGHT_EYE[8]]
        right_eye_landmark3 = landmarks[self.RIGHT_EYE[12]]
        right_eye_landmark4 = landmarks[self.RIGHT_EYE[4]]

        left_eye_landmark1 = landmarks[self.LEFT_EYE[0]]
        left_eye_landmark2 = landmarks[self.LEFT_EYE[8]]
        left_eye_landmark3 = landmarks[self.LEFT_EYE[12]]
        left_eye_landmark4 = landmarks[self.LEFT_EYE[4]]

        right_eye_horizontal_distance = self.euclideanDistance(right_eye_landmark1, right_eye_landmark2)
        right_eye_vertical_distance = self.euclideanDistance(right_eye_landmark3, right_eye_landmark4)

        left_eye_horizontal_distance = self.euclideanDistance(left_eye_landmark1, left_eye_landmark2)
        left_eye_vertical_distance = self.euclideanDistance(left_eye_landmark3, left_eye_landmark4)

        right_eye_ratio = right_eye_horizontal_distance / right_eye_vertical_distance
        left_eye_ratio = left_eye_horizontal_distance / left_eye_vertical_distance

        return (right_eye_ratio + left_eye_ratio) / 2

    def run(self):
        while not self.stop_thread:
            ret, frame = self.video_capture.read()
            if not ret:
                break

            frame = cv2.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            results = self.face_mesh.process(rgb_frame)

            blink_detected = False  # Flag to track if a blink event occurred

            if results.multi_face_landmarks:
                mesh_coordinates = self.landmarksDetection(frame, results)
                frame = self.drawLandmarks(frame, mesh_coordinates)  # Draw landmarks
                eyes_ratio = self.blinkRatio(mesh_coordinates)

                # Display the ratio for debugging
                cv2.putText(frame, f"Ratio: {eyes_ratio:.2f}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                if eyes_ratio > self.HIGH_THRESHOLD and not self.eyes_closed:
                    self.eyes_closed = True  # Eyes are now closed
                    # print("Eyes Closed")

                elif eyes_ratio < self.LOW_THRESHOLD and self.eyes_closed:
                    self.eyes_closed = False  # Eyes are now open
                    # print("Eyes Open")
                    current_time = time.time()

                    # Blink detected
                    if current_time - self.last_blink_time < 1:  # Double blink threshold
                        
                        # self.blink_queue.put("DOUBLE_BLINK")
                        try:
                            self. blink_queue.put("DOUBLE_BLINK", block=False)  # Non-blocking put
                        except queue.Full:
                            # print("Queue is full. Dropping item.")
                            pass

                        # print("Double Blink Detected")
                        blink_detected = True
                    elif current_time - self.last_single_blink_time >= self.COOLDOWN_PERIOD:

                        # Emit single blink only if cooldown has passed
                        # self.blink_queue.put("SINGLE_BLINK")
                        try:
                            self. blink_queue.put("SINGLE_BLINK", block=False)  # Non-blocking put
                        except queue.Full:
                            # print("Queue is full. Dropping item.")
                            pass

                        # print("Single Blink Detected")
                        blink_detected = True
                        self.last_single_blink_time = current_time

                    self.last_blink_time = current_time

            # If no blink was detected, send an empty string
            if not blink_detected:
                # self.blink_queue.put("")
                try:
                    self. blink_queue.put("", block=False)  # Non-blocking put
                except queue.Full:
                    # print("Queue is full. Dropping item.")
                    pass

            # Display the frame with landmarks and ratio
            # cv2.imshow("Blink Detection with Landmarks", frame)

            if cv2.waitKey(2) == 10:
                break

        self.video_capture.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.stop_thread = True
