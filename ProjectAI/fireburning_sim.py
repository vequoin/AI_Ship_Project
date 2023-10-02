import random


class Fire:

    def __init__(self, ship, q, start_cell) -> None:
        self.ship = ship
        self.q = q
        self.start_cell = start_cell
        self.cells_on_fire = set()
        self.cells_on_fire.add(self.start_cell)
    
    def spread_fire(self):
        next_cells_on_fire = set()
        for cell in self.cells_on_fire:
            all_neighbor_cells = self.ship.get_open_neighbors(cell)
            for curr_cell in all_neighbor_cells:
                if curr_cell not in self.cells_on_fire:
                    neighbors_on_fire = self.get_burning_neighbors(curr_cell)
                    k = len(neighbors_on_fire)
                    catch_probability = 1- (1 - self.q)**k
                    if random.random() < catch_probability:
                        next_cells_on_fire.add(curr_cell)
        self.cells_on_fire.update(next_cells_on_fire)
    
    
    def get_burning_neighbors(self,burning_cell):
        valid_neighbors = self.ship.get_open_neighbors(burning_cell)
        return [cell for cell in valid_neighbors if cell in self.cells_on_fire]
    
    def get_cells_on_fire(self):
        return self.cells_on_fire

