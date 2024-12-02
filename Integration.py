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
        player_Coords = None
        for ind, cards in enumerate(pred_cards):
            if len(cards) == 1:
                dealer = cards
                pred_cards.remove(cards)
                players = pred_cards
                player_Coords = card_groups[:ind] + card_groups[ind+1:]
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

        # On the original image draw the bounding box as well as the action to take for each player based on the
        # action list. Place the action near the bounding box for that player.
        # Action List: 0 -> Stand, 1 -> Hit, 2 -> Double Down
        for i in range(len(player_Coords)):
            x1, y1, x2, y2 = player_Coords[i]
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # Convert action to string for display based on the action list
            out = "Stand" if action_list[i] == 0 else "Hit" if action_list[i] == 1 else "Double Down"
            cv2.putText(img, out, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imwrite("out/predictions.jpg", img)

        return action_list

    def blackjack_game(self):
        Game = True
        while Game:
            Hand = True
            while Hand:
                # Load the image
                image = cv2.imread('test_images/card_detect.jpg')

                # Call the Integration method
                integration = Integration()
                prediction = integration.compute(image)
                print(prediction)

                Input = input("Y to continue, Done for standing")
                if Input == "Done":
                    Game = False

            Condi = True
            while Condi:
                Input = input("Has hand been resolve? Y/n")
                if Input == "Y":
                    Condi = False

            # Game is concluded - get final image from table
            image_table = cv2.imread('test_images/final_table.jpg')

            card_groups = self.card_detection.DectectCards(image_table)
            print(card_groups)

            # Get the card prediction
            pred_cards = []
            for card_group in card_groups:
                x1, y1, x2, y2 = card_group
                card = image_table[y1 - 100:y2 + 100, x1 - 100:x2 + 100]
                pred_cards.append(self.prediction.predict(card)[1])

            for card_group in pred_cards:  # Iterate through all card groups in image
                for card in card_group:  # iterate through all the cards
                    card = card.replace("c", "").replace("s", "").replace("h", "").replace("d", "")
                    card_rank_enum = A.CardRank(card)
                    self.algorithm.remove_card_from_shoe(card_rank_enum)
            Input = input("Game over? Y/n")
            if (Input == Y):
                Game = False
        


if __name__ == "__main__":
    Integration.blackjack_game(Integration)

