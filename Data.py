"""
Author: Soham Gandhi & Anthony Diaz
Date Created: 10/16/2024
Version: 1.0
Description: This file will load in the image data from the camera feed and return the images
"""

import kagglehub

class Data:
    def __init__(self):
        self.path = kagglehub.dataset_download("jaypradipshah/the-complete-playing-card-dataset")

    def get_data(self) -> str:
        """
        This function will return the path to the dataset
        :return: path
        """
        print("Path to dataset files:", self.path)
        return self.path


if __name__ == "__main__":
    data = Data()
    data.get_data()
