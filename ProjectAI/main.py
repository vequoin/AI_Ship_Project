from Ship import Ship
from fireburning_sim import Fire
from bot import Bot
from GameManager import GameManager
import random

get_ship_size = 25
q = .5
bot_strategy = "7"

def main():
    '''get_ship_size = int(input("Please enter your ship size: "))
    q = float(input("Enter the probability of fire:  "))
    bot_strategy = input("Enter a strategy: ")'''
    wins = 0
    losses = 0
    wins_shortest_path = 0
    loss_shortest_path = 0
    for i in range(20):
        game = GameManager(get_ship_size, q, bot_strategy)
        verdict = game.runGame()
        if verdict == "W":
            wins += 1
        elif verdict == "T":
            wins_shortest_path += 1
        elif verdict == "S":
            loss_shortest_path += 1
        else:
            losses += 1
    print(f"Losses: {losses} and Wins: {wins} ShortestPath: {wins_shortest_path}  LossesSP: {loss_shortest_path}")
