import socket
import random
from network2 import *
from gamefile import *
from REALGAME import *
import time

#define server IP address and port:
server = '127.0.0.1'
port = 5555


def main():
    print('in main')
    net = Network()     #Connect to the server and initialize the network
    print(net.id)
    print('connected')
    print('you are client number',net.id)
    result = net.send('join')     #send a message to the server to join the game and initialize the game state
    game = Game([result[1:(len(result))-1:1].split(',')])
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

            while player1_action <= 0 or player1_action >= len(game.player1):
                print("Invalid input. Please choose valid card indices.")
                player1_action = int(input("Player 1, choose a card index: "))
                value_player1 = game.values[game.player1[player1_action - 1].split()[1]]

            result = net.send('submit1,'+str(player1_action))
            print(result)
            while result == 'False':
                time.sleep(0.2)
                result = net.send('submit1,'+str(player1_action))
            print('player 2 played:',game.player2[int(result)-1] )


        elif game.player2Submitted == 'False' and net.id == '2':
            player2_action = int(input("Player 2, choose a card index: "))

            while player2_action <= 0 or player2_action >= len(game.player1):
                print("Invalid input. Please choose valid card indices.")
                player2_action = int(input("Player 2, choose a card index: "))
                value_player2 = game.values[game.player2[player2_action - 1].split()[1]]

            result = net.send('submit2,'+str(player2_action))
            while result == 'False':
                time.sleep(0.2)
                result = net.send('submit2,'+str(player2_action))
            print('player 1 played:',game.player1[int(result)-1] )

            if player2_action > player1_action:
                if net.id == '1':
                    result = net.send(game.discard.append(game.player1.pop(player1_action - 1)))
                    print(f"Player 1, your hand is {game.player1}")
                else:
                    result= net.send(game.discard.append(game.player2.pop(player2_action - 1)))
                    print(f"Player 2, your hand is {game.player2}")

            if value_player2 < value_player1:
                if net.id == '2':
                    print('Player 2 choose higher card')
                    print(f"Player 1, your hand is {game.player2}")
                else:
                    print(f"Player 2, your hand is {game.player2}")

            if value_player2 == 14 or value_player1 == 14:
                    print("Ace played! Moving to the next round.")
                    game.rounds_played += 1
                    result = net.send('round',game.rounds_played)
                    game.currenthand.append(game.player1)
                    game.currenthand.append(game.player2)
                    if net.id =='1':
                        print(f"Player 1, your hand is {game.player1}")
                    else:
                        print(f"Player 2, your hand is {game.player2}")

            if value_player1 < game.values[game.discard[len(game.discard)-1].split()[1]]:
                    print('play a card higher than the previous card')

                    player1_action = input('play or undo ')
                    player2_action = input('play or undo ')

                    if player1_action or player2_action == 'undo':
                        game.undo(player1_action,player2_action,game.currenthand)

            else:
                print("Invalid input for one or both players. Please choose valid card indices.")



main()
