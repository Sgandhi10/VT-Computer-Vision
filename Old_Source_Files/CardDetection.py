"""
Author: Anthony Diaz
Date Created: 11/10/2024
Version: 1.0
Description: Contains CardDection functionality to then return segmentation of cards
"""
import numpy as np
from PIL import Image
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import cv2



class CardDection:
    @staticmethod
    def detectcard(img_array):
        # Convert image to grayscale
        image = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
        image = cv2.GaussianBlur(image, (15, 15), 1)

        # Define color bounds for masking
        lower_bound = np.array([215])    # Adjust these values
        upper_bound = np.array([255])  # Adjust these values

        # Create the mask and segment the image
        mask = cv2.inRange(image, lower_bound, upper_bound)
        segmented_image = cv2.bitwise_and(image, image, mask=mask)
        
        # # Export the segmented image
        # cv2.imwrite("out/mask.jpg", mask)

        # # Display results
        # plt.subplot(1, 3, 1)
        # plt.imshow(image, cmap="gray")
        # plt.title("Original Image")

        # plt.subplot(1, 3, 2)
        # plt.imshow(mask, cmap="gray")
        # plt.title("Mask")

        # plt.subplot(1, 3, 3)
        # plt.imshow(segmented_image, cmap="gray")
        # plt.title("Segmented Image")

        # plt.show()

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Minimum size for width and height of the blob
        min_width = 800
        min_height = 800
        
        # Color image for drawing rectangles
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        # Draw rectangles around each contour that meets the size criteria
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w >= min_width or h >= min_height:  # Check if the blob is big enough
                cv2.rectangle(mask, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # # Export the image with rectangles
        cv2.imwrite("out/rectangles.jpg", mask)
        


# Read file in as RGB
img_array = cv2.imread("test_images/card_detect2.jpg")
CardDection.detectcard(img_array)


