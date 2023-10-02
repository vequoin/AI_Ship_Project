from Ship import Ship
from bot import Bot
from fireburning_sim import Fire
import random

class GameManager:
    def __init__(self, ship_size, probability,bot_strategy):
        self.ship = Ship(ship_size)
        self.bot_position, self.fire_position, self.button_position = self.initialize_game_elements()
        self.fire = Fire(self.ship, probability, self.fire_position)
        self.bot = Bot(self.ship, bot_strategy,self.bot_position, self.button_position)  
        
    def initialize_game_elements(self):
        open_cells = self.ship.open_cells.copy()
        
        # Randomly fetching positions for bot, fire and button
        bot_position = random.choice(open_cells)
        open_cells.remove(bot_position)
        
        fire_position = random.choice(open_cells)
        open_cells.remove(fire_position)
        
        button_position = random.choice(open_cells)
        
        return bot_position, fire_position, button_position
    
    def runGame(self):
        
        if self.bot.strategy == "1":
            getPath = self.bot.get_shortest_path
            step = 0
            while self.bot.is_alive:
                self.bot.move(getPath[0])
                step += 1
                


