import pytest

from bj import BlackJackGame
from deck import Deck 
from participants import Player

class Test_BlackJackGame(object):
    game = BlackJackGame('player')
    deck = Deck()
    player = Player('ernesto', 500)

    def test_check_points(self):
        cards1 = ['10S','9H']
        cards2 = ['JS','KH']
        cards3 = ['4H','AC']
        cards4 = ['10S','AH','KS']
        cards5 = ['10S']
        cards6 = ['AH']
        cards7 = []
        assert self.game.check_points(cards1) == 19
        assert self.game.check_points(cards2) == 20
        assert self.game.check_points(cards3) == 15
        assert self.game.check_points(cards4) == 21
        assert self.game.check_points(cards5) == 10
        assert self.game.check_points(cards6) == 11
        assert self.game.check_points(cards7) == 0

    def test_check_if_blown(self):
        cards1 = ['10S','AH','KS']
        cards2 = ['10S','8H','7S']
        cards3 = ['10S','10H','2S']
        assert self.game.check_if_blown(cards1) == False 
        assert self.game.check_if_blown(cards2) == True
        assert self.game.check_if_blown(cards3) == True  

    def test_give_cards(self):
        self.game.give_cards(self.player, self.deck, 4)
        assert self.player.hand == ['KS', 'KC', 'KH', 'KD']
        self.game.give_cards(self.player, self.deck, 2)
        assert self.player.hand == ['KS', 'KC', 'KH', 'KD', 'QS', 'QC']
        self.player.empty_hand()
        assert self.player.hand == []
        assert len(self.deck.deck) == 46




