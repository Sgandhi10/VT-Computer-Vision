import unittest

import Algorithm
from Algorithm import *
import random

class virtual_deck:
    def __init__(self):
        self.deck_list=['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']*4*8
        random.shuffle(self.deck_list)  # Shuffle the deck when it's created
        self.Alori = Algorithm()

    # draws a random card and removes it from deck_list
    def draw_card(self)->CardRank:
        card = self.deck_list.pop()
        print(self.deck_list)
        print(card)
        return CardRank(card)

    def deck_total(self):
        return len(self.deck_list)

def test_bruh():
        player_total = 0
        hands_played = 0
        algo = Algorithm(8)
        deck = virtual_deck()
        while (deck.deck_total() > 100):
            dealer_cards = []
            dealer_cards.append(deck.draw_card())
            player_cards = []
            player_cards.append(deck.draw_card())
            player_cards.append(deck.draw_card())

            player_action = True

            doubled = 1
            while(player_action):
                action = algo.action(dealer_cards[0], player_cards)
                if(action == 0): # stand
                    player_action = False
                elif(action == 1): # hit
                    player_cards.append(deck.draw_card())
                elif(action == 2): #double
                    player_cards.append(deck.draw_card())
                    player_action = False
                    doubled = 2
            if sum(card.worth() for card in dealer_cards) > 21:
                player_total += 1*doubled
            else:
                while (sum(card.worth() for card in dealer_cards) < 17):
                    dealer_cards.append(deck.draw_card())
                    if deck.deck_total() == 0:
                        break
                deal_number = sum(card.worth() for card in dealer_cards)
                player_number = sum(card.worth() for card in player_cards)
                if  deal_number > 21:
                    player_total += 1*doubled
                elif deal_number == player_number:
                    continue
                elif player_number>deal_number:
                    player_total += 1*doubled
                elif deal_number>player_number:
                    player_total -=1*doubled
            hands_played +=1
            for card in player_cards:
                algo.remove_card_from_shoe(card)
            for card in dealer_cards:
                algo.remove_card_from_shoe(card)
        algo.print_show()
        print("Player value left: "+str(player_total))
        return player_total, hands_played

class TestAlgorithm(unittest.TestCase):
    #TODO write more tests for algo to see if they follow basic strategy
    def test_getEV_Algo(self):
        ev = []
        hands_played = 0
        for i in range(30):
            bets_change, hands = test_bruh()
            ev.append(bets_change)
            hands_played = hands_played + hands
        print("Total bets change: " + str(sum(ev)))
        print("Total of hands played: " + str(hands_played))


if __name__ == '__main__':
    unittest.main()
