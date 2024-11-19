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
        # Load the image
        image = img_array

        # Convert to HSV
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define color bounds for masking
        lower_bound = np.array([0, 0, 200])    # Adjust these values
        upper_bound = np.array([180, 20, 255])  # Adjust these values

        # Create the mask and segment the image
        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
        segmented_image = cv2.bitwise_and(image, image, mask=mask)

        # Display results
        plt.subplot(1, 3, 1)
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title("Original Image")

        plt.subplot(1, 3, 2)
        plt.imshow(mask, cmap="gray")
        plt.title("Mask")

        plt.subplot(1, 3, 3)
        plt.imshow(cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB))
        plt.title("Segmented Image")

        plt.show()


img_array = mpimg.imread("test_images/8C40.jpg")
CardDection.detectcard(img_array)


