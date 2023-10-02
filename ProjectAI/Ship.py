import random


class Ship:
    def __init__(self, D):
        self.name = "Archaeopteryx"
        self.D = D
        self.ship = self.generate_ship()
        self.fire_instance = None
        self.open_cells = self.get_open_cells()

    def generate_ship(self):
        ship = [[1 for _ in range(self.D)] for _ in range(self.D)]

        start_cell = (random.randint(0, self.D - 1), random.randint(0, self.D - 1))
        ship[start_cell[0]][start_cell[1]] = 0

        fringe_cells = set(self.get_neighbors(start_cell))

        while fringe_cells:
            valid_cells = [cell for cell in fringe_cells if ship[cell[0]][cell[1]] and sum([1 - ship[nx][ny] for nx, ny in self.get_neighbors(cell)]) == 1]

            if not valid_cells:
                break

            chosen_cell = random.choice(valid_cells)
            ship[chosen_cell[0]][chosen_cell[1]] = 0

            fringe_cells.remove(chosen_cell)
            fringe_cells.update(self.get_neighbors(chosen_cell))

        self.eliminate_dead_ends(ship)
        return ship

    def eliminate_dead_ends(self, ship):
        dead_ends = [(row, col) for row in range(self.D) for col in range(self.D) if
                     ship[row][col] == 0 and sum([1 - ship[nx][ny] for nx, ny in self.get_neighbors((row, col))]) == 1]

        for dead_end in dead_ends:
            if random.random() > 0.5:
                potential_blocks = [cell for cell in self.get_neighbors(dead_end) if ship[cell[0]][cell[1]] == 1]
                if potential_blocks:
                    block_to_open = random.choice(potential_blocks)
                    ship[block_to_open[0]][block_to_open[1]] = 0

    def get_open_cells(self):
        return [(i, j) for i, row in enumerate(self.ship) for j, cell in enumerate(row) if cell == 0]

    def get_neighbors(self, cell):
        x, y = cell
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [(xi, yi) for xi, yi in neighbors if 0 <= xi < self.D and 0 <= yi < self.D]

    def get_open_neighbors(self, cell):
        x, y = cell
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        valid_cells = [(xi, yi) for xi, yi in neighbors if 0 <= xi < self.D and 0 <= yi < self.D and self.ship[xi][yi] == 0]
        return valid_cells


    #def __str__(self):
        #return "\n".join(" ".join(str(cell) for cell in row) for row in self.ship)
    
    def __str__(self):
        grid_str = ""
        for i, row in enumerate(self.ship):
            for j, cell in enumerate(row):
                if self.fire_instance and (i, j) in self.fire_instance.get_cells_on_fire():
                    grid_str += "F "
                elif cell == 0:
                    grid_str += "0 "
                else:
                    grid_str += "1 "
            grid_str += "\n"
        return grid_str
