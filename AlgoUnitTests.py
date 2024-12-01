import unittest
from Algorithm import *

class TestAlgorithm(unittest.TestCase):
    #TODO write more tests for algo to see if they follow basic strategy
    def test_bruh(self):
        algo = Algorithm(8)
        expected_values = algo.action(CardRank.TEN, [CardRank.SIX, CardRank.TEN])
        for action in expected_values:
            print(str(action) + ": " + str({expected_values[action]}))

if __name__ == '__main__':
    unittest.main()