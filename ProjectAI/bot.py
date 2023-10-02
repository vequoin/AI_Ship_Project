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

    def get_shortest_path(self):
        visited = set()
        queue = deque([([self.position], self.position)])  # Storing both path and the current node in the queue
        
        while queue:
            path, current = queue.popleft()
            if current == self.button_position:
                return path  # return the path when button_position is reached
            if current in visited:
                continue
            visited.add(current)
            
            for neighbor in self.ship.get_open_neighbors(current):
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append((new_path, neighbor))
        
        return None  # Return None if there is no path to the button_position
    
    def get_shortest_path_two(self):
        visited = set()
        queue = deque([[self.position]])  # queue to hold all paths; initially it has one path with only the start node
    
        while queue:
            path = queue.popleft()  # getting the first path from the queue
            current = path[-1] # getting the last cell

            if current == self.button_position:  
                return path  # return the entire path if we found the button

            if current in visited:  # if we already visited this node in another path, skip it
                continue 
            
            visited.add(current)  # mark the node as visited

            neighbours = [cell for cell in self.maze.get_open_neighbors(current) if cell not in visited]
            for neighbour in neighbours:  
                new_path = list(path)  # create a new path extending the current one
                new_path.append(neighbour)  # add the neighbor to the new path
                queue.append(new_path)  # enqueue the new path

            return None  # return None if there is no path to the button




    def play(self, bot_number):
        if bot_number == 1:
            self.strategy = self.get_shortest_path()
        elif bot_number == 2:
            pass
    

