import socket
import random
import network2

import REALGAME
import time

#define server IP address and port:
server = '127.0.0.1'
port = 1234


def main():
    print('in main')
    net = network2.Network()   #Connect to the server and initialize the network
    print(net.id)
    print('connected')
    print('you are client number',net.id)
    #result = net.send('join')    #send a message to the server to join the game and initialize the game state
    game = REALGAME.Game()
    game.player1 = sorted(game.deck[0:26])
    game.player2 = sorted(game.deck[26:52])
    if net.id == '1':
        print(game.player1) #uses game id to determine which set of hands to send to whcih player
    else:
        print(game.player2)

    game_complete = False   # boolean value that remains false until the game is running
    allready = False        # helpful for keeping the game logic running until game is complete

    while allready == False:
        time.sleep(0.2)
        result = net.send('allready')
        if result == 'True':    # checks both client connections to make sure player is ready
            allready = True

    while game_complete == False:  # keeps the game loop going
        game.rounds_played += 1    # keeping track of the rounds played
        if game.player1Submitted == 'False' and net.id == '1':    # going to player 1 first and if a card has not been played
            player1_action = int(input("Player 1, choose a card index: "))  # prompts them to play a card

            # checks that a valid card has been selected , and if not ot promps you to pick another
            # it will then split the index and take th value of the card
            #it then assigns a value_player1 the value of card picked
            #making it easier for comparison with player 2's cards

            while player1_action <= 0 or player1_action >= len(game.player1):
                print("Invalid input. Please choose valid card indices.")
                player1_action = int(input("Player 1, choose a card index: "))
                value_player1 = game.values[game.player1[player1_action - 1].split()[1]]

            #sends a message to the server using the net object.
            # informs the server about the action taken by player 1. The response
            #from the server is stored in the result variable.
            result = net.send('submit1,'+str(player1_action))
            print(result)
            while result == 'False':
                time.sleep(0.2)
                result = net.send('submit1,'+str(player1_action))
            print('player 2 played:',game.player2[int(result)-1] )

        # continues to player 2 and asks for a card , assuming that the game is not complete
        # and that the player is player number 2
        elif game.player2Submitted == 'False' and net.id == '2':
            player2_action = int(input("Player 2, choose a card index: "))

            #validates the card that has been chosen , like we did with player 1
            #stores the card value in value_player2

            while player2_action <= 0 or player2_action >= len(game.player1):
                print("Invalid input. Please choose valid card indices.")
                player2_action = int(input("Player 2, choose a card index: "))
                value_player2 = game.values[game.player2[player2_action - 1].split()[1]]

            #sends a message to the server using the net object.
            # informs the server about the action taken by player 2. The response
            #from the server is stored in the result variable.

            result = net.send('submit2,'+str(player2_action))
            while result == 'False':
                time.sleep(0.2)
                result = net.send('submit2,'+str(player2_action))
            print('player 1 played:',game.player1[int(result)-1] )


            # if statement to check if what player 2 has played is valid
            if player2_action > player1_action:
                if net.id == '1':
                    #both players have played valid cards, the cards that were played are popped out of their respective
                    #hands. the unpdated version is then sent to the server
                    result = net.send((game.player1.pop(player1_action - 1)))
                    print(f"Player 1, your hand is {game.player1}")
                else:
                    result= net.send(game.discard.append(game.player2.pop(player2_action - 1)))
                    print(f"Player 2, your hand is {game.player2}")

            #if invalid cards are played then it just asks them so player a higher card

            if value_player2 < value_player1:
                if net.id == '2':
                    print('Player 2 choose higher card')
                    print(f"Player 1, your hand is {game.player2}")
                else:
                    print(f"Player 2, your hand is {game.player2}")

            # an ace is the highest card you can play, and so if one is played you move to th enext round


            if value_player2 == 14 or value_player1 == 14:
                    print("Ace played! Moving to the next round.")
                    game.rounds_played += 1
                    result = net.send('round',game.rounds_played)
                    game.currenthand.append(game.player1)
                    game.currenthand.append(game.player2)
                    # information about the rounds is updated and sent to the server
                    if net.id =='1':
                        print(f"Player 1, your hand is {game.player1}")
                    else:
                        print(f"Player 2, your hand is {game.player2}")
            # to keep the round going , you just keep adding a card higher than the previous card
            # function to check that this is actually happening
            if value_player1 < game.values[game.discard[len(game.discard)-1].split()[1]]:
                    print('play a card higher than the previous card')

                    player1_action = input('play or undo ')
                    player2_action = input('play or undo ')

                    #players can either continue playing or one player may decide to undo their action.
                    # in that case the previous hands are returned.
                    if player1_action or player2_action == 'undo':
                        game.undo(player1_action,player2_action,game.currenthand)

            else:
                print("Invalid input for one or both players. Please choose valid card indices.")

main()
