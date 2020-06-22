import random

'''
Black Jack game
By: Ada Del Cid
Based on Project 2 of the Udemy course: 'Complete Python Bootcamp: Go from zero to hero in Python 3' by Jose Portilla
'''

SUITS = ['Hearts', 'Clubs', 'Spades', 'Diamonds']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
VALUES = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

class Chips():
    def __init__(self,total = 100):
        '''Player's chips and bet'''
        self.total = total
        self.bet = 0

    def win_bet(self):
        '''adjusts player's total if the player wins bet'''
        self.total += self.bet

    def lose_bet(self):
        '''adjusts player's total if the player loses bet'''
        self.total -= self.bet

class Card():
    def __init__(self,suit,rank):
        '''Creates an object card given suit and rank'''
        self.suit = suit
        self.rank = rank

    def __str__(self):
        '''returns string that describes card object'''
        return self.rank + ' of ' + self.suit

class Deck():
    def __init__(self):
        '''Creates a deck of cards'''
        self.deck = []
        for suit in SUITS: #for each suit
            for rank in RANKS: #for each rank
                self.deck.append(Card(suit,rank)) #add a new card to the deck

    def shuffle(self):
        '''shuffles the deck of cards'''
        random.shuffle(self.deck)
    
    def deal(self):
        '''deals one card from the cards remaining in the deck'''
        card_dealt = self.deck.pop()
        return card_dealt

class Hand():
    def __init__(self):
        '''Saves the player or dealer's card hand, their value and the number of aces'''
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self,card):
        '''Adds a card to the player or dealer's hand'''
        self.cards.append(card)
        self.value += VALUES[card.rank]
        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_aces(self):
        '''Adjusts the value if the dealer or player go over 21 and have aces'''
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

def take_bet(chips):
    '''Takes player's bet'''
    while True:
        try:
            chips.bet = int(input("Please place a bet:"))
        except:
            print("Please place a valid bet, must be an integer!")
        else:
            if chips.total >= chips.bet:
                break
            else:
                print("Sorry your bet cannot exceed your available chips " + str(chips.total))

def hit(deck,hand):
    '''Adds cards to hand and updates value'''
    card = deck.deal()
    hand.add_card(card)
    hand.adjust_for_aces()
    
def hit_or_stand(deck,hand):
    '''Asks player is they want to hit or stand'''
    global playing
    while True:
        user_input = input("Player, do you want to hit ('h') or stand ('s')?")

        if len(user_input) != 0 and user_input[0].lower() == 'h':
            hit(deck,hand)
        elif len(user_input) != 0 and user_input[0].lower() == 's':
            print("Player stands, Dealer is playing.")
            playing = False
        else:
            print("Sorry, please try again.")
            continue
        break

def show_some(player,dealer):
    '''Shows all player's card and 1 of the dealer's cards'''
    print("\nDealer's Hand:")
    print("<Hidden card>")
    print("", dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep ='\n')

def show_all(player,dealer):
    '''Shows all the cards of both dealer and player'''
    print("\nDealer's Hand:",*dealer.cards,sep = '\n')
    print("Dealer's Hand:", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n')
    print("Player's Hand:",player.value)

def player_busts(player,dealer,chips):
    '''Displays that player busted and updates chips'''
    print("Player busts!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    '''Displays that player wins and updates chips'''
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    '''Displays that dealer busts and updates player's chips'''
    print("Dealer busts!")
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    '''Displays that dealer wins and updates player's chips'''
    print("Dealer wins!")
    chips.lose_bet()

def push(player,dealer):
    '''Displays that it's a tie'''
    print("Dealer and Player tie! It's a push")

if __name__ == "__main__":
    #Saves if current play is the first play or restart
    first = True

    while True:
        print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
            Dealer hits until she reaches 17. Aces count as 1 or 11.')

        # Create & shuffle the deck, deal two cards to each player
        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())

        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        # Set up the Player's chips on first play
        if first:
            player_chips = Chips()  # remember the default value is 100

        # Prompt the Player for their bet
        take_bet(player_chips)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        while playing:  # recall this variable from our hit_or_stand function

            # Prompt for Player to Hit or Stand
            hit_or_stand(deck, player_hand)

            # Show cards (but keep one dealer card hidden)
            show_some(player_hand, dealer_hand)

            # If player's hand exceeds 21, run player_busts() and break out of loop
            if player_hand.value > 21:
                player_busts(player_hand, dealer_hand, player_chips)
                break

        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        if player_hand.value <= 21:

            while dealer_hand.value < 17:
                hit(deck, dealer_hand)

            # Show all cards
            show_all(player_hand, dealer_hand)

            # Run different winning scenarios
            if dealer_hand.value > 21:
                dealer_busts(player_hand, dealer_hand, player_chips)

            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand, player_chips)

            elif dealer_hand.value < player_hand.value:
                player_wins(player_hand, dealer_hand, player_chips)

            else:
                push(player_hand, dealer_hand)

        # Inform Player of their chips total
        print("\nPlayer's winnings stand at", player_chips.total)

        # Ask to play again
        new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")

        if new_game[0].lower() == 'y' and player_chips.total > 0 :
            first = False
            playing = True
            player_chips = Chips(player_chips.total)
            continue
        elif player_chips.total == 0:
            replay = input("Player is out of chips! Would you like to reset and play again? Enter 'y' or 'n'")
            if replay[0].lower() == 'y':
                first = True
                playing = True
                continue
            else:
                print("Thanks for playing!")
                break
        else:
            print("Thanks for playing!")
            break