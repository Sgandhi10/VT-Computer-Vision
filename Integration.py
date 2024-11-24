import Card_Detection as CD
import Prediction as P
import Algorithm as A
import Camera


import cv2
import numpy as np

class Integration:
    def __init__(self):
        self.camera = Camera.Camera()
        self.card_detection = CD.Card_Detection()
        self.prediction = P.Prediction()
        self.algorithm = A.Algorithm()

    def get_frame(self) -> np.ndarray:
        """
        This function will return the frame from the camera using a generator
        :return: frame
        """
        while True:
            frame = next(self.camera.get_frame())
            yield frame

    def release(self):
        self.camera.release()
        cv2.destroyAllWindows()

    def run(self):
        for frame in self.get_frame():
            cards = self.card_detection.DectectCards(frame)
            for card in cards:
                x1, y1, x2, y2 = card
                card_img = frame[y1:y2, x1:x2]
                prediction = self.prediction.predict(card_img)
                if prediction:
                    self.algorithm.run(prediction)
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.release()
        cv2.destroyAllWindows()
