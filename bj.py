import copy
from deck import Deck 
from participants import Dealer, Player

class BlackJackGame():
    bet_history  = [0]

    def __init__(self, player:Player , dealer:Dealer):
        self.player = player 
        self.dealer = dealer 


    @staticmethod
    def check_points(cartas):
        cartas = copy.deepcopy(cartas)
        real = [x[:-1] for x in cartas]
        sum_digits = sum(int(x) for x in real if x.isdigit())
        letters = [x for x in real if not x.isdigit()]
        n_values = {'J':10, 'Q':10, 'K': 10}
        a_max = {'A':11} ; a_min = {'A':1}
        a_max.update(n_values) ; a_min.update(n_values)
        letter_val_min = sum(a_min[x] for x in letters)
        letter_val_max = sum(a_max[x] for x in letters)
        total_min = min(sum_digits+letter_val_max, sum_digits+letter_val_min)
        total_max = max(sum_digits+letter_val_max, sum_digits+letter_val_min)
        return total_min if total_max > 21 else total_max

    def print_points(self):
        p_points = self.check_points(self.player.hand)
        d_points = self.check_points(self.dealer.hand)
        print('{} points ------- > {}'.format(self.player.name.title(), p_points))
        print('{} points ------- > {}'.format(self.dealer.name.title(), d_points))
        

    def print_player_status(self):
        print(self.player)
        bet_str = 'Bet :'.ljust(15) + str(self.bet_history[-1]).rjust(15)
        print(bet_str)
        string  = 'Hand:'.ljust(5) + Deck.print_cards(self.player.hand).rjust(25)
        print(string)
        string = 'Total points'.ljust(15) + str(self.check_points(self.player.hand)).rjust(15)
        print(string)

    def print_dealer_status(self):
        print(self.dealer)
        string  = 'Hand:'.ljust(15) + Deck.print_cards(self.dealer.hand).rjust(15)
        print(string)
        string = 'Total points'.ljust(15) + str(self.check_points(self.dealer.hand)).rjust(15)
        print(string)

    def check_player_dealer_points(self):
        player_points = self.check_points(self.player.hand)
        dealer_points = self.check_points(self.dealer.hand)
        return (player_points, dealer_points)
        

    def check_if_blown(self, cartas):
        return True if self.check_points(cartas) > 21 else False 

    @staticmethod
    def give_cards(player:Player, deck:Deck, number):
        player.give_cards(deck.pull_cards(number))

    def check_odds(self, deck:Deck, player:Player, n_attemps = 5000):
        """ check the odds of now going above 21 """
        blown = 0
        for x in range(n_attemps):
            deck_copy = copy.deepcopy(deck)
            deck_copy.shuffle()
            player_copy = copy.deepcopy(player)
            self.give_cards(player_copy, deck_copy, 1)
            if self.check_if_blown(player_copy.hand):
                blown += 1
        return int(((n_attemps - blown)/n_attemps)*100)


    def check_odds_covering_dealer(self, deck:Deck, player:Player, dealer:Dealer, n_attemps = 5000):
        covered = 0
        dealer_points = self.check_points(dealer.hand)
        for _ in range(n_attemps):
            deck_copy = copy.deepcopy(deck)
            player_copy = copy.deepcopy(player)
            deck_copy.shuffle()
            self.give_cards(player_copy, deck_copy, 1)
            if dealer_points <= self.check_points(player_copy.hand) < 22:
                covered += 1 
        return int((covered / n_attemps)*100)

    def odds_hitting_21(self, deck:Deck, player:Player, n = 5000):
        hit =  0
        for _ in range(n):
            deck_copy = copy.deepcopy(deck)
            deck_copy.shuffle()
            player_copy = copy.deepcopy(player)
            self.give_cards(player_copy, deck_copy, 1)
            if self.check_points(player_copy.hand) == 21:
                hit += 1
        return int((hit/n)*100)

    def check_total_odds(self, deck:Deck, n = 10000):
        blown = 0 
        hit_21 = 0 
        cover_dealer = 0
        dealer_points = self.check_points(self.dealer.hand)
        for _ in range(n):
            deck_copy = copy.deepcopy(deck)
            deck_copy.shuffle()
            player_copy = copy.deepcopy(self.player)
            self.give_cards(player_copy, deck_copy, 1)
            if self.check_if_blown(player_copy.hand):
                blown += 1
            if dealer_points <= self.check_points(player_copy.hand) < 22:
                cover_dealer += 1
            if self.check_points(player_copy.hand) == 21:
                hit_21 += 1
        prob_n_blown = int(((n - blown)/n)*100)
        prob_cover_dealer = int((cover_dealer / n)*100)
        prob_hit_21 = int((hit_21/n)*100)
        return prob_n_blown, prob_cover_dealer, prob_hit_21

            






if __name__ == '__main__':

    ernesto = Player('Ernesto', 500)
    dealer = Dealer('Dealer', 500)
    g1 = BlackJackGame(ernesto, dealer)
    deck = Deck()
    deck.shuffle()
    g1.give_cards(dealer, deck, 2)
    g1.give_cards(ernesto, deck, 2)
    g1.print_player_status()
    g1.print_dealer_status()
    print(g1.check_odds(deck, ernesto, 10000))
    print(g1.check_odds_covering_dealer(deck, ernesto, dealer))
    print(g1.odds_hitting_21(deck, ernesto))
    print(g1.check_total_odds(deck))



