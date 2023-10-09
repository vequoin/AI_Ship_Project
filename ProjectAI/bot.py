import random
from collections import deque
from Ship import Ship

class Bot:
    def __init__(self, ship, bot_number,position, button_position):
        self.ship = ship
        self.position = position
        self.button_position = button_position
        self.strategy = bot_number
        self.is_alive = True
    
    def move(self, position):
        self.position = position
        
   
    def get_possible_moves(self):
        open_neighbors = self.ship.get_open_neighbors()
        

    '''def play(self, bot_number):
        if bot_number == 1:
            self.strategy = self.get_shortest_path()
        elif bot_number == 2:
            self.strategy = self.get_shortest_path()
            pass'''
    

