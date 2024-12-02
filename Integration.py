import Card_Detection as CD
import Prediction as P
import Algorithm as A
import re

import cv2
import numpy as np

class Integration:
    def __init__(self):
        self.card_detection = CD.Card_Detection()
        self.prediction = P.Prediction()
        self.algorithm = A.Algorithm()

    def compute(self, img):
        """
        This function will return the card prediction
        :return: prediction
        """
        # Get the card groups
        card_groups = self.card_detection.DectectCards(img)
        print(card_groups)

        # Get the card prediction
        pred_cards = []
        for card_group in card_groups:
            x1, y1, x2, y2 = card_group
            card = img[y1-100:y2+100, x1-100:x2+100]
            pred_cards.append(self.prediction.predict(card)[1])

        print(pred_cards)

        dealer = None
        players = None
        for cards in pred_cards:
            if len(cards) == 1:
                dealer = cards
                pred_cards.remove(cards)
                players = pred_cards
                break

        if dealer is None:
            print("No dealer found")
            return None

        print(dealer)
        print(players)
        dealer = list(dealer)
        # Convert list of string card values to card Enum Values
        Dealer_Card = dealer[0]
        Dealer_Card = Dealer_Card.replace("c","").replace("s", "").replace("h","").replace("d","")
        Dealer_Card = A.CardRank(Dealer_Card)

        # list of actions from algo
        action_list = []
        for player in players:  # Iterates through all players
            player_cards = [] # cards for player
            for card in player:
                card = card.replace("c","").replace("s", "").replace("h","").replace("d","")
                card_rank_enum = A.CardRank(card)
                player_cards.append(card_rank_enum)
            action_list.append(self.algorithm.action(Dealer_Card, player_cards))


        return action_list


if __name__ == "__main__":
    # Load the image
    image = cv2.imread('test_images/card_detect.jpg')

    # Call the Integration method
    integration = Integration()
    prediction = integration.compute(image)

    print(prediction)
