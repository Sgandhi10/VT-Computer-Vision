"""
Author: Soham Gandhi
Date Created: 10/16/2024
Version: 1.0
Description: This file will read in the camera feed and return the image
"""

import cv2
import numpy as np

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def get_frame(self) -> np.ndarray:
        """
        This function will return the frame from the camera using a generator
        :return: frame
        """
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            else:
                yield frame

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    camera = Camera()
    for frame in camera.get_frame():
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()

