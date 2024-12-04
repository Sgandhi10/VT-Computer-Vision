from Card_Detection import Card_Detection
from Prediction import Prediction
import os
import cv2

# For every card in test_images/Card_Detection/Input folder
# Go through every image in folder:

pd = Prediction()

for img in os.listdir('test_images/Card_Detection/Input'):
    # Load the image
    image = cv2.imread('test_images/Card_Detection/Input/' + img, cv2.IMREAD_COLOR)

    # Get the card groups
    card_groups = Card_Detection.DectectCards(image)
    print(card_groups)

    # output image
    image_out = image.copy()

    # Get the card prediction
    pred_cards = []
    for card_group in card_groups:
        x1, y1, x2, y2 = card_group
        b_box = 200
        x1 = max(0, x1 - b_box)
        y1 = max(0, y1 - b_box)
        y2 = min(y2 + b_box, image.shape[0])
        x2 = min(x2 + b_box, image.shape[1])
        card = image[y1:y2, x1:x2]
        pred_cards.append(pd.predict(card)[1])

        # Draw bounding box around every card group and state card prediction for group
        cv2.rectangle(image_out, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image_out, str(pred_cards[-1]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 255, 0), 5)
    cv2.imwrite("test_images/Card_Detection/Output/" + img, image_out)
    print(pred_cards)
    print("Image saved as test_images/Card_Detection/Output/" + img)
    print("\n")
