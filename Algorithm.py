'''
Description: Algorithm handles probability and expected value calculations while returning
the action that maximizes expected value
'''
from enum import Enum


class CardRank(Enum):
    """Represents a rank of a playing card.
    
    value -- 1-string symbol for this rank, may contain point value information
    """
    ACE = "A"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"

    def worth(self) -> int:
        """Retrieves the point value of this rank.
        Aces can count as either 1 or 11 depending on context; corresponding logic is accounted
        for elsewhere in relevant functions.
        """
        match self:
            case CardRank.ACE:
                return 11
            case CardRank.TEN | CardRank.JACK | CardRank.QUEEN | CardRank.KING:
                return 10
            case _:
                return int(self.value)


class Action(Enum):
    """Represents a possible player action.
    """
    STAND = 0
    HIT = 1
    DOUBLE = 2


class Algorithm:
    """Contains the main algorithm that determines player choice in blackjack, as well as
    lasting state that tracks the contents of the dealer's shoe.
    
    shoe -- the dealer's current remaining cards
    """

    class Shoe:
        """Stores card information to enable the use of card-counting techniques in blackjack
        calculations. Card suits are not used in standard blackjack, and therefore not tracked
        in this class.

        num_decks -- the number of 52-card decks that are combined to form this shoe
        rank_counts -- a mapping of card rank to the amount of that card rank present in this shoe
        """
        
        def __init__(self, num_decks):
            self.num_decks = num_decks
            self.rank_counts: dict[CardRank, int] = dict()
            self.initialize_shoe()
        
        def initialize_shoe(self) -> None:
            """Resets this shoe.  Upon initialization of this shoe, each rank appears 4 times for
            each deck.
            """
            self.rank_counts = {rank: self.num_decks * 4 for rank in [cr.value for cr in CardRank]}
        
        def remove_card(self, rank: CardRank) -> None:
            """Removes a card from this shoe.
            
            rank -- the rank of the card being removed
            
            ValueError -- if this shoe does not contain the specified rank
            """
            if self.rank_counts[rank] == 0:
                raise ValueError(f"{rank} already has zero cards in shoe")
            
            self.rank_counts[rank] -= 1

    def __init__(self, num_decks: int = 6):
        self.shoe = self.Shoe(num_decks)


    def remove_card_from_shoe(self, shown_card: CardRank) -> None:
        """Removes a card from the shoe. 

        shown_card -- the rank of the card being removed

        ValueError -- if this shoe does not contain the specified rank
        """
        self.Shoe.remove_card(shown_card)

    def action(self, dealer_card: CardRank, player_cards: list[CardRank]) -> int:
        """Determines the expected value of each player action given a blackjack state.  Each EV
        is returned in a dictionary with Action keys (i.e. hit, stand, and double).

        dealer_card -- the card the dealer is showing
        player_cards -- list of the cards that the player has
        """
        # can dealer hit blackjack?
        dealer_can_blackjack = False
        # manages soft totals, where aces can change from 11 to 1 within a total
        player_soft_total = False
        dealer_soft_total = False

        # calculate player total
        player_total = 0
        for card in player_cards:
            player_total += card.worth()
            # for aces, we automatically add 11, but there is special logic
            if card is CardRank.ACE:
                player_soft_total = True
                if player_total > 21:  # handles if player has two aces
                    player_total -= 10

        # calculate dealer total
        dealer_total = dealer_card.worth()
        if dealer_total == 10:
            dealer_can_blackjack = True
        elif dealer_total == 11:
            dealer_can_blackjack = True
            dealer_soft_total = True

        # EV: 0 = push, 1 = win, -1 = loss, 2 = double win, -2 = double loss
        hit_expected_result = self.expected_value_hit(self.shoe.rank_counts, dealer_total, player_total, False,
                                                      player_soft_total, dealer_soft_total, dealer_can_blackjack)
        stand_expected_result = self.expected_value_stand(self.shoe.rank_counts, dealer_total, player_total, False,
                                                          dealer_soft_total, dealer_can_blackjack)
        double_expected_result = self.expected_value_hit(self.shoe.rank_counts, dealer_total, player_total, True,
                                                         player_soft_total, dealer_soft_total, dealer_can_blackjack)

        highest_ev = max(hit_expected_result, stand_expected_result, double_expected_result)

        if highest_ev == stand_expected_result:
            return Action.STAND.value
        elif highest_ev == hit_expected_result:
            return Action.HIT.value
        elif highest_ev == double_expected_result:
            return Action.DOUBLE.value

        # return {
        #     Action.HIT: hit_expected_result,
        #     Action.STAND: stand_expected_result,
        #     Action.DOUBLE: double_expected_result,
        # }

    def expected_value_hit(self, shoe_state: dict[CardRank, int],
                           dealer_total: int, player_total: int,
                           is_doubled: bool,
                           player_soft_total: bool, dealer_soft_total: bool, dealer_can_blackjack: bool) -> float:
        """Calculates the EV of hitting once. Does so by going through every possible series of
        player cards and every possible series of dealer cards. Recursively called. See action()
        comment for EV explanation.

        shoe_state -- the rank counts in this shoe
        dealer_total -- the point value of the card the dealer is showing
        player_total -- the current point total of the player's cards
        is_doubled -- whether the player doubled, which prevents another hit but doubles the EV

        VTL?
        """
        expected_value = 0
        # total number of cards in shoe = number of cards that could be dealt
        total_cards_in_shoe = sum(shoe_state[rank] for rank in shoe_state)
        # adjusts bet for correct expected value if doubled or not
        bet_absolute_value = 2 if is_doubled else 1

        # iterates through all possible ranks
        for shown_rank in shoe_state.keys():
            # how many of the rank are in the shoe?
            total_of_rank_in_shoe = shoe_state[shown_rank]

            # if it's zero, we don't have to worry about this timeline. otherwise...
            if total_of_rank_in_shoe != 0:
                # ...how likely was this rank to appear? (weight)
                fraction_of_all_outcomes = total_of_rank_in_shoe / total_cards_in_shoe

                # new_shoe_state represents the hypothetical shoe after *this* potential hit
                new_shoe_state = dict(shoe_state)  # copy to a new dictionary
                new_shoe_state[shown_rank] -= 1  # if we saw a card, there's one less in the shoe now

                # establish a new player total after this hit
                shown_rank_value = CardRank(shown_rank).worth()
                new_player_total = player_total + shown_rank_value

                # if next card is an ace...
                if shown_rank == "A":
                    if new_player_total > 21:  # ...and the 11 puts the player over 21...
                        new_player_total -= 10  # ...the ace becomes a 1
                    else:  # ...and the 11 keeps the player under or at 21...
                        player_soft_total = True  # ...then the 11 can still become a 1

                # adjusts new_player_total if it goes over 21 with a soft total
                if new_player_total > 21 and player_soft_total:
                    new_player_total -= 10  # ace becomes a 1
                    player_soft_total = False  # this can never be true again

                # evaluating expected value based on new_player_total
                if new_player_total > 21:  # automatic loss
                    expected_value += -1 * bet_absolute_value * fraction_of_all_outcomes
                elif new_player_total == 21 or is_doubled:  # automatic stand
                    expected_value += self.expected_value_stand(new_shoe_state, dealer_total, new_player_total, is_doubled,
                                                                dealer_soft_total, dealer_can_blackjack) * fraction_of_all_outcomes
                else:  # chooses the optimal play post-hit, as that will give us the optimal play here
                    ev_when_hit = self.expected_value_hit(new_shoe_state, dealer_total, new_player_total, False,
                                                          player_soft_total, dealer_soft_total, dealer_can_blackjack)
                    ev_when_stand = self.expected_value_stand(new_shoe_state, dealer_total, new_player_total, False,
                                                              dealer_soft_total, dealer_can_blackjack)
                    expected_value += max(ev_when_hit, ev_when_stand) * fraction_of_all_outcomes

        return expected_value

    def expected_value_stand(self, shoe_state: dict[CardRank, int],
                             dealer_total: int, player_total: int,
                             is_doubled: bool,
                             dealer_soft_total: bool, dealer_can_blackjack: bool) -> float:
        """Calculates the EV after standing. Does so by going through every possible series of
        dealer cards. Recursively called. See action() comment for EV explanation.

        shoe_state -- the rank counts in this shoe
        dealer_total -- the point total of the dealer's cards
        player_total -- the point total of the player's cards
        is_doubled -- whether the player doubled, which doubles the EV

        VTL? rest of docstring
        """
        expected_value = 0
        # total number of cards in shoe = number of cards that could be dealt
        total_cards_in_shoe = sum(shoe_state[rank] for rank in shoe_state)
        # adjusts bet for correct expected value if doubled or not
        bet_absolute_value = 2 if is_doubled else 1

        # iterates through all possible ranks
        for shown_rank in shoe_state:
            # how many of the rank are in the shoe?
            total_of_rank_in_shoe = shoe_state[shown_rank]

            # if it's zero, we don't have to worry about this timeline. otherwise...
            if total_of_rank_in_shoe != 0:
                # ...how likely was this rank to appear? (weight)
                fraction_of_all_outcomes = total_of_rank_in_shoe / total_cards_in_shoe

                # new_shoe_state represents the hypothetical shoe after *this* potential dealer hit
                new_shoe_state = dict(shoe_state)  # copy to a new dictionary
                new_shoe_state[shown_rank] -= 1  # if we saw a card, there's one less in the shoe now

                # establish a new dealer total after this dealer hit
                shown_rank_value = CardRank(shown_rank).worth()
                new_dealer_total = dealer_total + shown_rank_value
                
                # if next card is an ace...
                if shown_rank == "A":
                    if new_dealer_total > 21:  # ...and the 11 puts the dealer over 21...
                        new_dealer_total -= 10  # ...the ace becomes a 1
                    else:  # ...and the 11 keeps the dealer under or at 21...
                        dealer_soft_total = True  # ...then the 11 can still become a 1
            
                # adjusts new_dealer_total if it goes over 21 with a soft total
                if new_dealer_total > 21 and dealer_soft_total:
                    new_dealer_total -= 10  # ace becomes a 1
                    dealer_soft_total = False  # this can never be true again
                
                if new_dealer_total > 21:  # automatic win
                    expected_value += bet_absolute_value * fraction_of_all_outcomes
                elif new_dealer_total == 21 and dealer_can_blackjack:  # dealer hits blackjack
                    expected_value += -1 * bet_absolute_value * fraction_of_all_outcomes
                # elif new_dealer_total == 17 and dealer_soft_total:  # soft 17, dealer hits again
                #     expected_value += self.expected_value_stand(new_shoe_state, new_dealer_total, player_total, is_doubled,
                #                                                 dealer_soft_total, False) * fraction_of_all_outcomes
                elif new_dealer_total >= 17 and player_total > new_dealer_total:  # automatic win
                    expected_value += bet_absolute_value * fraction_of_all_outcomes
                elif new_dealer_total >= 17 and new_dealer_total > player_total:  # automatic loss
                    expected_value += -1 * bet_absolute_value * fraction_of_all_outcomes
                elif new_dealer_total >= 17 and new_dealer_total == player_total:  # automatic push
                    expected_value += 0
                else:  # the dealer has to keep going, but the next card could be any remaining in the shoe
                    expected_value += self.expected_value_stand(new_shoe_state, new_dealer_total, player_total, is_doubled,
                                                                dealer_soft_total, False) * fraction_of_all_outcomes
        
        return expected_value


# Testing
if __name__ == "__main__":
    Algo = Algorithm()
    Algo.action()
