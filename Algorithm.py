'''
Description: Algorithm handles probability and expected value calculations while returning
the action that maximizes expected value
'''
from enum import Enum
from ultralytics import YOLO
import torch

class CardRank(Enum):
    ACE = "A"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "T"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"

    def worth(self) -> list[int]:
        # value of card, keeping in mind aces
        match self:
            case CardRank.ACE:
                return [1, 11]
            case CardRank.TEN | CardRank.JACK | CardRank.QUEEN | CardRank.KING:
                return [10]
            case _:
                return [int(self.value)]


class Action(Enum):
    STAND = 0
    HIT = 1
    DOUBLE = 2


class Algorithm:
    class Shoe:
        def __init__(self, num_decks:int=6):
            self.num_decks = num_decks
            self.rank_counts: dict[CardRank, int] = {}
            self.initialize_deck()
        
        def initialize_deck(self) -> None:
            self.rank_counts = {self.num_decks * 4 for rank in [cr.value for cr in CardRank]}
        
        def remove_card(self, rank: str) -> None:
            if not self.rank_counts.has_key(rank):
                raise ValueError(f"{rank} is not a card rank")
            elif self.rank_counts[rank] == 0:
                raise ValueError(f"{rank} already has zero cards in shoe")
            
            self.rank_counts[rank] -= 1


    def __init__(self):
        print(torch.cuda.is_available())
        if torch.cuda.is_available():
            print(f"GPU: {torch.cuda.get_device_name(0)} is available.")
        else:
            print("No GPU available. Training will run on CPU.")

        # Load the model
        self.model = YOLO('yolov8n_custom_final.pt')

        self.shoe = self.Shoe(num_decks=1)


    def action(self, dealer_card: CardRank, player_cards: list[CardRank]) -> dict[Action, float]:
        # TODO: make sure cards are removed from the shoe object, but don't remove the same card twice

        dealer_total = dealer_card.worth()
        player_total = sum(card.worth() for card in player_cards)

        # ev: 0 = push, 1 = win, -1 = loss, 2 = double win, -2 = double loss
        hit_expected_result = self.expected_value_hit(self.shoe.rank_counts, dealer_total, player_total, False)
        stand_expected_result = self.expected_value_stand(self.shoe.rank_counts, dealer_total, player_total, False)
        double_expected_result = self.expected_value_hit(self.shoe.rank_counts, dealer_total, player_total, True)

        return {
            Action.HIT: hit_expected_result,
            Action.STAND: stand_expected_result,
            Action.DOUBLE: double_expected_result,
        }

    def expected_value_hit(self, shoe_state: dict[CardRank, int], dealer_total: int, player_total: int, doubled: bool) -> float:
        # we chose to hit. assuming we play optimally the rest of the way, how good was the hit?

        expected_value = 0
        total_cards_in_shoe = sum(list(shoe_state))
        bet_absolute_value = 2 if doubled else 1

        for shown_rank in shoe_state:  # what happens if this rank is shown when we hit?
            total_of_rank_in_shoe = shoe_state[shown_rank]  # how many of the rank are in the shoe?
            if total_of_rank_in_shoe != 0:  # if it's zero, we don't have to worry about this timeline. otherwise...
                fraction_of_all_outcomes = total_of_rank_in_shoe / total_cards_in_shoe  # ...how likely was this rank to appear? (weight)
                new_shoe_state = dict(shoe_state)  # copy to a new dictionary
                new_shoe_state[shown_rank] -= 1  # if we saw a card, there's one less in the shoe now

                new_player_total = player_total + shown_rank  # TODO: aces, this code doesn't work bc worth returns multiple values
                if new_player_total > 21:  # automatic loss
                    expected_value += -1 * bet_absolute_value * fraction_of_all_outcomes  # L
                elif new_player_total == 21 or doubled:  # automatic stand
                    expected_value += self.expected_value_stand(new_shoe_state, dealer_total, new_player_total, doubled)
                else:  # the player can hit or stand. which one is better?
                    ev_when_hit = self.expected_value_hit(new_shoe_state, dealer_total, new_player_total, False)
                    ev_when_stand = self.expected_value_stand(new_shoe_state, dealer_total, new_player_total, False)
                    expected_value += max(ev_when_hit, ev_when_stand)

        return expected_value

    def expected_value_stand(self, shoe_state: dict[CardRank, int], dealer_total: int, player_total: int, doubled: bool) -> float:
        expected_value = 0
        total_cards_in_shoe = sum(list(shoe_state))
        bet_absolute_value = 2 if doubled else 1

        for shown_rank in shoe_state:  # what happens if the dealer shows this card?
            total_of_rank_in_shoe = shoe_state[shown_rank]  # how many of the rank are in the shoe?
            if total_of_rank_in_shoe != 0:  # if it's zero, we don't have to worry about this timeline. otherwise...
                fraction_of_all_outcomes = total_of_rank_in_shoe / total_cards_in_shoe  # ...how likely was this rank to appear? (weight)
                new_shoe_state = dict(shoe_state)  # copy to a new dictionary
                new_shoe_state[shown_rank] -= 1  # if we saw a card, there's one less in the shoe now

                new_dealer_total = dealer_total + shown_rank  # TODO: aces
                if new_dealer_total > 21:  # automatic win
                    expected_value += bet_absolute_value * fraction_of_all_outcomes
                elif new_dealer_total >= 17 and player_total > new_dealer_total:  # automatic win
                    expected_value += bet_absolute_value * fraction_of_all_outcomes
                elif new_dealer_total >= 17 and new_dealer_total > player_total:  # automatic loss
                    expected_value += -1 * bet_absolute_value * fraction_of_all_outcomes
                elif new_dealer_total >= 17 and new_dealer_total == player_total:  # automatic push
                    expected_value += 0
                else:  # the dealer has to keep going, but the next card could be any remaining in the shoe
                    expected_value += self.expected_value_stand(new_shoe_state, new_dealer_total, player_total, doubled)
