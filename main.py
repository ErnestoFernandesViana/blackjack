from deck import Deck 
from participants import Player, Dealer
from bj import BlackJackGame
import json 
import time

""" opens json file to check if user already exists"""
with open('users.json') as jfile:
    users_dict = json.load(jfile)

"""Ask for user name """
player_name = input("What's your name?")
if player_name.lower() in users_dict:
    player_balance = users_dict[player_name.lower()]
    if player_balance == 0:
        users_dict[player_name.lower()] = 500

else:
    player_balance = 500
    new_user = {player_name.lower() : player_balance}
    users_dict.update(new_user)

json_dict = json.dumps(users_dict)
with open('users.json', 'w') as file:
    file.write(json_dict)

""" create player, dealer and game instance """
player = Player(player_name, player_balance)
dealer = Dealer('Dealer', 500)
game = BlackJackGame(player, dealer)
""" run the game """
while True:
    if player.money == 0:
        break 
    answer = input(f'You are starting with ${player.money}. Would you like to play a hand?(y/n)')
    if answer == 'n':
        break 
    else:
        while True:
            bet = int(input('Place your bet!'))
            if bet == 0:
                print('Minimun value is $1.')
                continue
            if player.lose_money(bet):
                dealer.lose_money(bet)
                game.bet_history.append(bet)
                break
        player.empty_hand()
        dealer.empty_hand()
        deck = Deck()
        deck.shuffle()
        game.give_cards(player, deck, 2)
        game.give_cards(dealer, deck, 2)
        print('\n')
        game.print_player_status()
        print('\n')
        game.print_dealer_status()
        p = game.check_player_dealer_points()
        print('\n')
        while True:
            p = 0,0
            if game.check_points(player.hand) > 11:
                odds = input('Want to know the odds of not going above 21 for $5?(y/n)')
                if odds == 'y':
                    odds_result = game.check_odds(deck, player, 2000)
                    print('The odds of hitting 21 or below are {}%.'.format(int(odds_result)))
                    player.lose_money(5)
            answer = input('Would you like to hit or stay?(h/s)')
            if answer == 'h':
                game.give_cards(player, deck, 1)
                game.print_player_status()
                time.sleep(1.5)
                if game.check_if_blown(player.hand):
                    print('You hit above 21')
                    dealer.win_money(bet*2)
                    break
                p = game.check_player_dealer_points()
                if p[0] > p[1]:           
                    print('Dealer hits \n')
                    game.give_cards(dealer, deck, 1)
                    game.print_dealer_status()
                    time.sleep(1.5)
                    if game.check_if_blown(dealer.hand):
                        print('Dealer blew above 21')
                        time.sleep(3)
                        player.win_money(bet*2)
                        break
                    continue
                elif p[0] < p[1]:
                    print("Dealer didn't hit")
                    game.print_dealer_status()
                    continue
                     
            elif answer == 's':
                p = game.check_player_dealer_points()
                if p[0] > p[1]:           
                    print('Dealer hits \n')
                    game.give_cards(dealer, deck, 1)
                    game.print_dealer_status()
                    time.sleep(1.5)
                    if game.check_if_blown(dealer.hand):
                        print('Dealer blew above 21')
                        time.sleep(3)
                        player.win_money(bet*2)
                        break
                    continue
                elif p[0] < p[1]:
                    print("Dealer didn't hit")
                    game.print_dealer_status()
                    continue
                game.print_points()
                time.sleep(1)
                p = game.check_player_dealer_points()
                if p[0] > p[1]:
                    print('You won!')
                    time.sleep(1)
                    player.win_money(bet*2)
                elif p[0] == p[1]:
                    print('Was a tie.')
                    time.sleep(1)
                    player.win_money(bet)
                    dealer.win_money(bet)
                elif p[0] < p[1]:
                    dealer.win_money(bet*2)
                    print('You lose!')
                    time.sleep(1)
                
                break 

print('Game has ended. Your balance will be saved!')
users_dict[player.name.lower()] = player.money
json_dict = json.dumps(users_dict)
with open('users.json', 'w') as file:
    file.write(json_dict)

if __name__ == '__main__':
    print(player)




""" add current bet to print output """