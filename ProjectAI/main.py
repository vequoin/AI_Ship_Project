from Ship import Ship
from fireburning_sim import Fire
from bot import Bot
import random
from jiji import 

def main():
    '''get_ship_size = int(input("Please enter your ship size: "))
    q = float(input("Enter the probability of fire:  "))
    bot_strategy = input("Please select a Strategy: \n Stategy 1) \t Strategy 2) \n Strategy 3) Strategy 4)")
    game = GameManager(get_ship_size, q, bot_strategy)
    game.runGame()
    print(game.ship.name)
    print(game.ship)'''
    ship = Ship(10)
    print(ship)

if __name__ == "__main__":
    main()
