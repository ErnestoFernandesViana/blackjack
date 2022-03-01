from deck import Deck

class Player:
    
    def __init__(self, name, money):
        self.name = name
        self._money = money 
        self.hand = []
    
    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, value):
        if 0 <= value <= 5000:
            self._money = value 
            return True 
        else:
            print('Money has to be a positive number below 5000!')
            return False 
    
    def lose_money(self, value):
        if self._money < value:
            print("Not enough money")
            return False
        else:
            self._money -= value 
            return True 

    def win_money(self, value):
        self._money += value 

    def give_cards(self, cartas):
        self.hand = self.hand + cartas

    def empty_hand(self):
        self.hand = []

    def __str__(self):
        full_str = []
        full_str.append(format(' '+self.name.title()+' ', '*^30'))
        size_balance = len(str(self._money))
        second_str = 'Total balance'.ljust(30-size_balance) + str(self._money).rjust(size_balance)
        full_str.append(second_str)
        return '\n'.join(full_str)

class Dealer(Player):
    def __init__(self, name, money):
        super().__init__(name, money)

    def lose_money(self, value):
        if self._money < value:
            print("Dealer doesn't have enough money")
            self._money = 0 
        else:
            self._money -= value 
            return True 






if __name__ == '__main__':
    p1 = Player('marcelo', 1600)
    print(p1.lose_money(100))
    p1.lose_money(300)
    print(p1.money)
    print(p1)
    d1 = Dealer('ernesto',1500)
    print(d1.hand)


""" Objective is to end the round with hand higher value than dealer
without going over 21.
Normal cards has their own value. JQK has value 10 and A has 1 or 11
If at any point hand is over 21 game is busted. 

Rules for the dealer. May be modified: If hand is over 17 the stay
if hand is 16 or less it hits. If hits over 21 it loses.

If the player has a blackjack ans dealer doesn't hit it. 1.5 times money returned

 """