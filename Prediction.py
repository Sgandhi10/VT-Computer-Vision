import cv2
import torch
from ultralytics import YOLO


class Prediction:
    def __init__(self):
        print(torch.cuda.is_available())
        if torch.cuda.is_available():
            print(f"GPU: {torch.cuda.get_device_name(0)} is available.")
        else:
            print("No GPU available. Training will run on CPU.")

        # Load the model
        self.model = YOLO('yolov8n_custom_final.pt')



    def predict(self, img):
        """
        This function will return the predictions for the image
        :return: predictions
        """
        # Pass the image through the detection model and get the result
        detect_result = self.model(img)

        matches = set()

        for result in detect_result:
            boxes = result.boxes  # Access the bounding boxes
            for box in boxes:
                # Get the bounding box coordinates
                x1, y1, x2, y2 = box.xyxy[0]

                # Get the class ID and confidence score
                class_id = box.cls[0].item()
                confidence = box.conf[0].item()

                # Get the class name
                class_name = self.model.names[class_id]
                matches.add(class_name)

                # print("Class:", class_name)
                # print("Confidence:", confidence)
                # print("Bounding box:", x1, y1, x2, y2)

        # Plot the detections
        detect_image = detect_result[0].plot()

        # Convert the image to RGB format
        detect_image = cv2.cvtColor(detect_image, cv2.COLOR_BGR2RGB)

        # Return the detected card names
        return detect_image, matches


if __name__ == "__main__":
    prediction = Prediction()
    img = cv2.imread("out/card_0.jpg", cv2.IMREAD_COLOR)
    pred, match = prediction.predict(img)
    cv2.imwrite("out/predictions1.jpg", pred)
    print(match)
    img = cv2.imread("out/card_1.jpg", cv2.IMREAD_COLOR)
    pred, match = prediction.predict(img)
    cv2.imwrite("out/predictions2.jpg", pred)
    print(match)