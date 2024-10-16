# VT-Computer-Vision
Computer Vision Project
Created by Soham Gandhi and Anthony Diaz

This is the main repo for Blackjack Vision, ECE 4554 project. This project aims to provide optimal player strategy for blackjack using computer vision.

The project is broken down into 3 main components: Card Detection, Card Interpretation, and Card Inference.

Card Detection will identify playing cards within an image in order to interpret their value. Likely done using OpenCV or similar library using either Line Detection or Color Masks.

Card Interpretation is identifying the card's 'value' from 2-10, Ace, King, Queen, and Jack. This maybe done using a trained CNN or YOLO.

Card Inference is leveraging the cards on the board and previous boards in order to calculate optimal decision for the player. We will calculate the expected value using probabilies based on remanining cards in deack for each decision in order to select which actions to take.





