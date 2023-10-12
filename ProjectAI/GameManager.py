from Ship import Ship
from bot import Bot
from fireburning_sim import Fire
from collections import deque
from Node import Node
import random

################################## Initializing Game Manager #################################################

class GameManager:
    def __init__(self, ship_size, q,bot_strategy):
        """
        Initialize the GameManager class which manages the game's overall state, 
        including the bot, fire spread, ship layout, and game elements' positions.

        Args:
            ship_size (int): The size (dimension) of the ship.
            q (float): Probability of fire spread to neighboring cells.
            bot_strategy (function): The strategy the bot uses to navigate.
        """
       
        self.ship = Ship(ship_size)  # Create a ship object with the given size.
        
        self.ship_length = ship_size  # Store the ship size.
        
        # Initialize positions for the bot, fire, and button.
        self.bot_position, self.fire_position, self.button_position = self.initialize_game_elements()
        
         # Set the fire spread probability.
        self.q = q  # Set the fire spread probability.
        
        # Create a Fire instance on the ship 
        self.fire = Fire(self.ship, q, self.fire_position)  

         # Store the selected bot strategy.
        self.bot_strategy = bot_strategy  

        # Create a Bot instance initialized with the ship, its strategy, and its initial and goal positions
        self.bot = Bot(self.ship, bot_strategy, self.bot_position, self.button_position)

        # Initialize a set to keep track of nodes (positions) that have been visited during pathfinding
        self.visited_nodes = set()  
        
    def initialize_game_elements(self):
        """
        Initialize the starting positions of the bot, fire, and button on the ship.
        
        Returns:
            tuple: Bot's position, fire's position, and button's position.
        """

        # Create a copy of all open (unoccupied) cells on the ship
        open_cells = self.ship.open_cells.copy()
        
        # Randomly fetching positions for bot, fire and button
        bot_position = random.choice(open_cells)
        open_cells.remove(bot_position)
        
        fire_position = random.choice(open_cells)
        open_cells.remove(fire_position)
        
        button_position = random.choice(open_cells)
        
        return bot_position, fire_position, button_position
    
    
    ################################## Helper Functions for Strategy 1,2,3 ###############################################
    
     
    def get_shortest_path_two(self):
        # Find the shortest path to the button using BFS.
        # Bot moves toward the button while avoiding cells already visited or on fire.
        visited = set()
        queue = deque([[self.bot.position]])  # queue to hold all paths; initially it has one path with only the start node
    
        while queue:
            path = queue.popleft()  # getting the first path from the queue
            current = path[-1] # getting the last cell

            if current == self.button_position:  
                return path  # return the entire path if we found the button

            if current in visited:  # if we already visited this node in another path, skip it
                continue 
            
            visited.add(current)  # mark the node as visited
            neighbours = [cell for cell in self.ship.get_open_neighbors(current) if cell not in visited]
            for neighbour in neighbours:  
                new_path = list(path)  # create a new path extending the current one
                new_path.append(neighbour)  # add the neighbor to the new path
                queue.append(new_path)  # enqueue the new path

        return None  # return None if there is no path to the button
        
    def get_better_short_path(self):
        # Find an improved path to the button, considering the fire and visited cells.
        # Avoid cells that are on fire or have been visited.
        visited = set()
        queue = deque([[self.bot.position]])  # queue to hold all paths; initially it has one path with only the start node
    
        while queue:
            path = queue.popleft()  # getting the first path from the queue
            current = path[-1] # getting the last cell

            if current == self.button_position:
                return path  # return the entire path if we found the button

            if current in visited or current in self.fire.cells_on_fire:  # if we already visited this node in another path, skip it
                continue 
            
            visited.add(current)  # mark the node as visited

            neighbours = [cell for cell in self.ship.get_open_neighbors(current) if cell not in visited]
            for neighbour in neighbours:  
                new_path = list(path)  # create a new path extending the current one
                new_path.append(neighbour)  # add the neighbor to the new path
                queue.append(new_path)  # enqueue the new path

        return None  # return None if there is no path to the button
    
    
    def strategy_three_shortest_path(self):
        # Avoids the cells next to cells on fire
        path = self.find_path_strategy_three(True)
        if path:
            # Returns if the path is found
            return path
        else:
            # If no path is found, then try to find a path without avoiding the cells on fire
            return self.find_path_strategy_three(False)
    
    def find_path_strategy_three(self, avoiding):
        # Finds the shortest path for the third bot.
       
        visited = set()
        queue = deque([[self.bot.position]])  # queue to hold all paths; initially it has one path with only the start node
        rooms_to_avoid = self.cells_to_avoid(avoiding)
    
        while queue:
            path = queue.popleft()  # getting the first path from the queue
            current = path[-1] # getting the last cell

            if current == self.button_position:
                return path  # return the entire path if we found the button

            if current in visited or current in rooms_to_avoid:  # if we already visited this node in another path, skip it
                continue 
            
            visited.add(current)  # mark the node as visited

            neighbours = [cell for cell in self.ship.get_open_neighbors(current) if cell not in visited]
            for neighbour in neighbours:  
                new_path = list(path)  # create a new path extending the current one
                new_path.append(neighbour)  # add the neighbor to the new path
                queue.append(new_path)  # enqueue the new path

        return None  # return None if there is no path to the button
    
    
    ######################################## Strategy One #################################################
    
    
    def strategy_one(self):
        # The bot follows the shortest path without avoiding the fire.
        getPath = self.get_shortest_path_two()
        step = 0
        
        if not getPath: # Check if there is no path to the button
            print("There is no available path to the button.")
            return "L"

        game_won = False

        while self.bot.is_alive and not game_won:
            self.bot.move(getPath[step])
            step += 1

            if self.bot.position in self.fire.cells_on_fire:
                self.bot.is_alive = False
                print("Your bot has died in the fire! You have lost. Try again.")

            if self.button_position in self.fire.cells_on_fire:
                print("Button is on fire, you lost")
                return "L"

            self.fire.spread_fire()

            if self.bot.position == self.button_position:
                game_won = True
                print("Congratz you have saved the crew and the ship")

        if game_won:
            return "W"
        else:
            return "L"
        
        
        ######################################## Strategy Two #################################################
        
    def strategy_two(self):
        # The bot continuously seeks a better path to the button, adapting to the fire's spread.
        getPath = self.get_better_short_path()
        step = 1

        if not getPath:  # Check if there is no path to the button
            print("There is no available path to the button.")
            return "L"

        game_won = False
        while self.bot.is_alive and not game_won:
            new_path = self.get_better_short_path()
            if new_path != getPath:
                getPath = new_path
                step = 1
            if not getPath:
                print("There is no available Path for the bot, You loose")
                return "L"
            
            self.bot.move(getPath[step])
            step += 1
            if self.bot.position in self.fire.cells_on_fire:
                self.bot.is_alive = False
                print("Your bot has died in the fire! You have lost. Try again.")
            if self.button_position in self.fire.cells_on_fire:
                print("Button is on fire, you lost")
                return "L"
            self.fire.spread_fire()
            
            if self.bot.position == self.button_position:
                game_won = True
                print("Congratz you have saved the crew and the ship")
        if game_won:
            return "W"
        else:
            return "L"
        
    def cells_to_avoid(self, avoiding):
        # Identify cells to avoid during path calculation.
        # It considers cells on fire and optionally neighboring cells as well.
        fire_neighbors = set()
        for cell in self.fire.cells_on_fire:
            neighbors = self.ship.get_open_neighbors(cell)
            fire_neighbors.update(neighbors)
        if avoiding:
            return fire_neighbors.union(self.fire.cells_on_fire)
        else:
            return self.fire.cells_on_fire
        
        
    ########################################## Strategy Three ##################################################


    def strategy_three(self):
        # The bot continuously seeks a better path to the button, adapting to the fire's spread. It also avoids the cells that are next to the cells on fire
        getPath = self.strategy_three_shortest_path()
        step = 1
        
        if not getPath:  # Check if there is no path to the button
            print("There is no available path to the button.")
            return "L"

        game_won = False
        while self.bot.is_alive and not game_won:
            new_path = self.strategy_three_shortest_path()
            if new_path != getPath:
                getPath = new_path
                step = 1
            if not getPath:
                print("There is no available Path for the bot, You loose")
                return "L"
            
            self.bot.move(getPath[step])
            step += 1
            if self.bot.position in self.fire.cells_on_fire:
                self.bot.is_alive = False
                print("Your bot has died in the fire! You have lost. Try again.")
            if self.button_position in self.fire.cells_on_fire:
                print("Button is on fire, you lost")
                return "L"
            self.fire.spread_fire()
            #print(self)
            if self.bot.position == self.button_position:
                game_won = True
                print("Congratz you have saved the crew and the ship")
        if game_won:
            return "W"
        else:
            return "L"
        
    ########################################## Helper Functions Strategy 4 ##################################################
    

     # returns the manhatten distance of point 1 and point 2       
    def manhattan_distance(self, point1, point2):
        # Returns the Manhattan distance
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    
    def predict_fire_spread(self, depth):
        '''Predicts the spread of fire up to a depth of 5. It calculates the probability of which cells can catch fire after a certain number of turns 
        which are then assigned weights based on the probability calculated
        Args:
        depth (int): Number of steps (turns) ahead to predict.
    
        Returns:
        list: List of sets, where each set contains the cells predicted to catch fire at each depth.
        '''
         # Create a copy of the ship's current state
        generated = [row[:] for row in self.ship.ship]

        # Mark the current fire positions on the generated grid.
        for fire_cell in self.fire.cells_on_fire:
            generated[fire_cell[0]][fire_cell[1]] = 'F'

        current_fire_positions = self.fire.cells_on_fire.copy()
        all_fire_positions = set(current_fire_positions)  # To keep track of all fire positions
        future_fire_positions = []

        for i in range(depth):
            next_fire_spread = set()

            for cell in current_fire_positions:
                all_neighbor_cells = self.get_open_cells(cell, generated)
                for neighbor in all_neighbor_cells:
                    if neighbor not in all_fire_positions:  # Ensure fire doesn't spread to an already on-fire cell
                        k = sum(1 for adj_cell in self.get_neighbors(neighbor) if adj_cell in all_fire_positions)
                        catch_probability = 1 - (1 - self.q)**k
                        if random.random() < catch_probability:
                            next_fire_spread.add(neighbor)
                            generated[neighbor[0]][neighbor[1]] = 'F'
            
            if not next_fire_spread:
                break         
            future_fire_positions.append(next_fire_spread)
            current_fire_positions = next_fire_spread
            all_fire_positions.update(next_fire_spread)

        return future_fire_positions

    
    def get_open_cells(self, cell, ship):
        '''Gets all the open cells'''
        neighbors = self.get_neighbors(cell)
        return [neighbor for neighbor in neighbors if ship[neighbor[0]][neighbor[1]] == 0]

    def get_neighbors(self, cell):
        """Get all neighbors of a cell."""
        x, y = cell
        potential_neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        return [neighbor for neighbor in potential_neighbors if self.is_valid(neighbor)]

    def is_valid(self, cell):
        """Check if the cell is valid (within the ship's boundaries)."""
        x, y = cell
        m, n = len(self.ship.ship), len(self.ship.ship[0])
        return 0 <= x < m and 0 <= y < n
        
    def bfs_distance(self, start, target, fire_positions):
        '''
        Computes distance from start to target using BFS, avoiding fire_positions.
    
        Parameters:
        - start: Starting position (x, y).
        - target: Target position (x, y).
        - fire_positions: Set of fire positions.
    
        Returns: 
        - Shortest distance avoiding fire or infinity if not reachable.
        '''
        queue = [start]
        visited = set()
        visited.add(start)
        depth = 0

        while queue:
            current_level_size = len(queue)
            for i in range(current_level_size):
                current = queue.pop(0)
                if current == target:
                    return depth
                x, y = current
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.ship_length and 0 <= ny < self.ship_length:
                        if (nx, ny) not in visited and (nx, ny) not in fire_positions:
                            visited.add((nx, ny))
                            queue.append((nx, ny))
            depth += 1
        return float('inf')

    
    def bfs_distance_fire(self, start,fire, fire_positions):
        '''
        Computes distance from start to the nearest fire using BFS.
    
        Parameters:
        - start: Starting position (x, y).
        - fire: A fire position.
        - fire_positions: Set of fire positions.
    
        Returns:
        - Distance to the nearest fire or negative infinity if not reachable.
        '''
        # Uses BFS to give the distance from the bot to the fire
        queue = [start]
        visited = set()
        visited.add(start)
        depth = 0

        while queue:
            current_level_size = len(queue)
            for i in range(current_level_size):
                current = queue.pop(0)
                if current == fire:
                    return depth
                x, y = current
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.ship_length and 0 <= ny < self.ship_length:
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            queue.append((nx, ny))
            depth += 1
        return float('-inf')

    
    def calculate_fire_proximity(self, bot_position, fire_positions):
        """
        Calculate the distance from the bot to the nearest fire in each direction (up, down, left, right) using BFS.
    
        :param bot_position: A tuple indicating the current position of the bot.
        :param fire_positions: A list of tuples indicating the positions of all fires.
        :return: A dictionary containing the distance to the nearest fire for each valid direction.
        """
        proximity = {}
        for direction in ['up', 'down', 'left', 'right']:
            dx, dy = {
                'up': (-1, 0),
                'down': (1, 0),
                'left': (0, -1),
                'right': (0, 1)
            }[direction]
            next_position = (bot_position[0] + dx, bot_position[1] + dy)
            if next_position[0] < 0 or next_position[0] >= self.ship_length or next_position[1] < 0 or next_position[1] >= self.ship_length:
                continue
            if self.ship.ship[next_position[0]][next_position[1]] == 1:
                continue 
            # For each direction, find the closest fire.
            all_proximities = []
            if 0 <= next_position[0] < self.ship_length and 0 <= next_position[1] < self.ship_length:
                for fire in fire_positions:
                    all_proximities.append(self.bfs_distance_fire(next_position,fire, fire_positions))
                proximity[direction] = min(all_proximities)
            else:
                proximity[direction] = float('inf')
        return proximity

    
    ########################################## Strategy Four-Main functions ##################################################
    
    
    def calculate_path_based_on_risk(self, start, goal, risk_map):
         """
        Calculate the optimal path from start to goal based on risk values.
    
        :param start: A tuple indicating the starting position.
        :param goal: A tuple indicating the goal position.
        :param risk_map: A 2D list representing the risk values at each position.
        :return: A list of positions indicating the path from start to goal.
        """
        # Create a copy of the risk_map so as not to modify the original.
        temp_risk_map = [row.copy() for row in risk_map]

        # Define a penalty for visiting already visited nodes to discourage revisiting them.
        VISITED_PENALTY = 40
        for node in self.visited_nodes:
            x, y = node
            temp_risk_map[x][y] += VISITED_PENALTY

        # Initialize the open set with the start node, its path so far, and its g(n) value.
        open_set = [(start, [], 0)]  # Tuple: (position, path_so_far, g(n))
        visited = set()  # Set to keep track of visited nodes.
        
        while open_set:
            # Sort the open set based on the heuristic (f(n) = g(n) + h(n)).
            open_set.sort(key=lambda x: x[2] + self.manhattan_distance(x[0], goal))
            # Pop the node with the lowest f(n) value.
            current, path, g_n = open_set.pop(0)    
            if current == goal:
                return path 
            visited.add(current)
            neighbors = self.get_valid_moves(current)  # Assuming this method gives adjacent cells   
            for neighbor in neighbors:
                if neighbor not in visited:
                    risk = temp_risk_map[neighbor[0]][neighbor[1]]
                    new_path = list(path)
                    new_path.append(neighbor)
                    open_set.append((neighbor, new_path, g_n + risk))  
        return None  
    
    def create_risk_map(self, future_fire_positions):
        """
        Create a 2D risk map based on future fire positions.
    
        :param future_fire_positions: A list of lists, where each sublist contains the fire positions at a certain future time step.
        :return: A 2D list representing the risk values at each position.
        """
        risk_map = [[0 for _ in range(len(self.ship.ship[0]))] for _ in range(len(self.ship.ship))]
        for depth, cells in enumerate(future_fire_positions):
            # Calculate the risk value based on the depth (future time step).
            # The risk increases quadratically with the time step and is then multiplied by 10.
            # This is just one way of assigning risk, and it can be adjusted as needed.
            risk_value = ((depth*depth) + 1) * 10  # Example risk assignment. Adjust as needed.
            for cell in cells:
                risk_map[cell[0]][cell[1]] = risk_value
        return risk_map
            

    ########################################## Strategy Four ##################################################
                
    def strategy_four(self):
        """
        Strategy Four: Dynamic Risk Assessment and Adaptation

        Overview:
        This strategy dynamically evaluates the risks from predicted fire spread and adjusts the bot's path. 
        When the bot is closer to the goal and the path is clearer, it switches to Strategy Two for direct navigation.
    
        Steps:
        1. Compute fire proximity and shortest path to goal.
        2. If fire is far (over 1.75x distance to goal) or bot is near goal (Manhattan distance < 6 and BFS distance < 8), use Strategy Two.
        3. Predict fire spread over next 5 turns and create a 'risk map'.
        4. Determine optimal path using risk map. If no path is found, it's a loss.
        5. Move the bot based on the calculated path. After each move, fire spreads. Reaching the button means a win.
        """
        curr_position = self.bot.position
        proximity = self.calculate_fire_proximity(curr_position, self.fire.cells_on_fire)
        distance_to_goal = self.bfs_distance(curr_position, self.button_position, self.fire.cells_on_fire)
        proximity_danger = min(proximity.values())
        # If the closest fire is much farther than the goal (1.75 times the distance), switch to Strategy Two
        if proximity_danger > 1.75*distance_to_goal:
            return self.strategy_two()
        else:
            while self.bot.is_alive:
                curr_pos = self.bot.position
                # If bot is close to the goal (based on Manhattan distance) and bfs distance, switch to endgame phase and strategy 2. 
                if self.manhattan_distance(self.bot.position, self.button_position) < 6:
                    distance_to_goal = self.bfs_distance(curr_pos, self.button_position, self.fire.cells_on_fire)
                    if distance_to_goal < 8:
                        return self.strategy_two()
    
                proximity = self.calculate_fire_proximity(self.bot.position, self.fire.cells_on_fire)

                # Predict how the fire will spread over the next 5 turns
                future_fire_positions = self.predict_fire_spread(5)

                #create a risk map based on the predictions of fire spread
                risk_map = self.create_risk_map(future_fire_positions)
            
                self.visited_nodes.add(self.bot.position)
                
                # Calculate the path with current risk map
                path = self.calculate_path_based_on_risk(self.bot.position, self.button_position, risk_map)

                if not path:
                    print("There is no path to the button! You lost")
                    return "L"  # Loss if no path is found

                next_step = path[0]
                self.bot.move(next_step)
                self.fire.spread_fire()
                
                if next_step == self.button_position:
                    print("Congratz! you have saved the ship and the crew!")
                    return "W"  # Win if bot reached the button

     ############################################ Functions to execute different bots #######################################


      def runGame(self):
        self.ship.fire_instance = self.fire
        #game_won = False
        if self.bot_strategy == "1":
            return self.strategy_one()
        elif self.bot_strategy == "2":
            return self.strategy_two()
        elif self.bot_strategy == "3":
            return self.strategy_three()
        elif self.bot_strategy == "4":
            return self.strategy_four()
        elif self.bot_strategy == "5":
            return self.combo_strategy()
            
    # Prints the game Manager object , it prints the current state of the ship              
    def __str__(self):
        grid_str = ""
        for i, row in enumerate(self.ship.ship):  
            for j, cell in enumerate(row):
                if (i, j) in self.fire.cells_on_fire: 
                    grid_str += "F "
                elif (i, j) == self.bot.position:  
                    grid_str += "B "
                elif (i, j) == self.button_position:  
                    grid_str += "$ "
                elif cell == 0:
                    grid_str += "0 "
                else:
                    grid_str += "1 "
            grid_str += "\n"
        return grid_str
