import random

class Game:
    # This method is called when a new instance of the class is created.
    # It initializes the attributes of the class.
    # serves as a blueprint for representing the state of a card game
    def __init__(self,deck):
        self.currenthand = []
        self.player1 = []
        self.player2 = []
        self.discard = []
        self.rounds_played = 0
        self.values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    def buildDeck(self):
        #method that is called at the start of the game to set it up
        #initialises an empty deck , defines the suits and well as the ranks of the cards unisng a dictionary
        self.deck = []
        self.suits = ['spades', 'diamonds', 'hearts', 'clubs']
        self.values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        #Inside the nested loops, a string cardval is constructed
        # representing the combination of suit and value
        # Each cardval is appended to the self.deck array.
        for suit in self.suits:
            for value in self.values:
                cardval = "{} {}".format(suit, value)
                self.deck.append(cardval)

        random.shuffle(self.deck)  # shuffles the deck, mimicking what happens in real life
        #splits the shuffled eeck between two players and sorts them to make it easier
        self.player1 = self.deck[0:26]
        self.player2 = self.deck[26:52]
        self.player1 = sorted(self.player1)
        self.player2 = sorted(self.player2)

        #prints the players hands
        print(f"Player 1, your hand is {self.player1}")
        print(f"Player 2, your hand is {self.player2}")


    def play(self):
        self.buildDeck()   # initializes the deck of cards and distributes them among the players.
        while self.player1 and self.player2: # enters this loop as long as both players have cards
            self.rounds_played += 1 # rounds are incremeneted by one everytime an ace is played
            print(f"\nRound {self.rounds_played}")  # prints the current round
            # prints both players hands
            print(f"Player 1 hand: {self.player1}")
            print(f"Player 2 hand: {self.player2}")
            # a method call to handle the validity of player actions or moves
            self.acceptable()
        print("\nGame Over")
        print("Player 1's final hand:", self.player1)
        print("Player 2's final hand:", self.player2)
        print("Discard Pile:", self.discard)

    # handle the process of players choosing cards and
    # determining the outcome of their choices in the game
    def acceptable(self):
        while True:
            # prompts Players to choose a card index.
            player1_action = int(input("Player 1, choose a card index: "))
            player2_action = int(input("Player 2, choose a card index: "))
            self.currenthand.append(self.player1)
            self.currenthand.append(self.player2)

            #Both inputs are converted to integers for comparison and validation.
            #makes sure that the chosen indices are within the valid range of card indices for each player's hand.
            if 1 <= player1_action <= len(self.player1) and 1 <= player2_action <= len(self.player2):

                #The method extracts the values of the chosen cards from the players'
                # hands using the values dictionary and the card indices provided by the players.
                #It calculates the values of the chosen cards using the values dictionary
                value_player1 = self.values[self.player1[player1_action - 1].split()[1]]
                value_player2 = self.values[self.player2[player2_action - 1].split()[1]]

                #If Player 2's card value is higher than Player 1's, Player 2 wins the round.
                # Their cards are removed from their hands and added to the discard pile.

                if value_player2 > value_player1:
                    self.discard.append(self.player1.pop(player1_action - 1))
                    print(f"Player 1, your hand is {self.player1}")
                    self.discard.append(self.player2.pop(player2_action - 1))
                    print(f"Player 2, your hand is {self.player2}")

               #If Player 1's card value is higher, a message is printed indicating that Player 2
                # needs to choose a higher card.
                if value_player2 < value_player1:
                    print('Player 2 choose higher card')
                    print(f"Player 1, your hand is {self.player1}")
                    print(f"Player 2, your hand is {self.player2}")

                # if an ace is played , it is the highest card and therefore the rounds played increase by one
                if value_player2 == 14 or value_player1 == 14:
                    print("Ace played! Moving to the next round.")
                    self.rounds_played += 1
                    self.currenthand.append(self.player1)
                    self.currenthand.append(self.player2)
                    print(f"\nRound {self.rounds_played}")
                    print(f"Player 1, your hand is {self.player1}")
                    print(f"Player 2, your hand is {self.player2}")#

                #to ensure that the rounds are being collected, the cards have to played higher
                #than the previous one
                # you can then either continue to play or choose to undo your action

                if value_player1 < self.values[self.discard[len(self.discard)-1].split()[1]]:
                    print('play a card higher than the previous card')

                    player1_action = input('play or undo ')
                    player2_action = input('play or undo ')

                    if player1_action or player2_action == 'undo':
                        self.undo(player1_action,player2_action,self.currenthand)

            else:
                print("Invalid input for one or both players. Please choose valid card indices.")




    def undo(self,player1_action,player2_action,currenthand):

        if player1_action or player2_action == 'undo':
            try:
                value = currenthand.pop()
                #It updates the game state (discard pile, player hands)
                # based on the popped value to revert the game to its previous state.
                self.discard = self.currenthand.pop()
                self.player2 = self.currenthand.pop()
                self.player1 = self.currenthand.pop()
                # sends a message that undo was successful
                # prints out the unpdated list
                print("Undo successful.")
                print(f"Player 1, your hand is {self.player1}")
                print(f"Player 2, your hand is {self.player2}")
                print("Discard Pile:", self.discard)
                #recursive call to the acceptable method to allow the players to make their moves again.
                self.acceptable()

            except IndexError:
                print("No moves played to undo.")

def main():
    deck = buildDeck()  # You need to define this function to create the initial deck
    game = Game(deck)
    game.play()
    game = Game()
    game.play()
    game.buildDeck()

if __name__ == "__main__":
    main()
