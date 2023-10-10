import random


class Fire:

    def __init__(self, ship, q, start_cell) -> None:
        # Initializes a Fire object with its attributes.
        self.ship = ship  # Assigns the ship where the fire is spreading.
        self.q = q  # Sets the probability of fire spreading.
        self.start_cell = start_cell  # Sets the initial cell where the fire starts.
        self.cells_on_fire = set()  # Initializes a set to store cells currently on fire.
        self.cells_on_fire.add(self.start_cell)  # Adds the starting cell to the set of cells on fire.
    
    def spread_fire(self):
        # Simulates the spread of fire to neighboring cells based on the given probability.
        next_cells_on_fire = set()  # Create a set to store cells that will catch fire next.
        for cell in self.cells_on_fire:
            all_neighbor_cells = self.ship.get_open_neighbors(cell)  
            for curr_cell in all_neighbor_cells:
                if curr_cell not in self.cells_on_fire:
                    neighbors_on_fire = self.get_burning_neighbors(curr_cell)  # Get neighbors that are already on fire.
                    k = len(neighbors_on_fire)  # Count the number of burning neighbors.
                    fire_probability = 1 - (1 - self.q) ** k  
                    if random.random() < fire_probability:  # Check if fire spreads based on probability.
                        next_cells_on_fire.add(curr_cell)  
        self.cells_on_fire.update(next_cells_on_fire)  
    
    def get_burning_neighbors(self,burning_cell):
        # Returns the neighboring cells of a burning cell that are already on fire.
        valid_neighbors = self.ship.get_open_neighbors(burning_cell)
        return [cell for cell in valid_neighbors if cell in self.cells_on_fire]
    
    def get_cells_on_fire(self):
        # Returns the set of cells currently on fire.
        return self.cells_on_fire

