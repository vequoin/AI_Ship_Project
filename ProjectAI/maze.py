import random

class Maze:
    def __init__(self, D):
        self.D = D
        self.maze = self.generate_maze()
        self.open_cells = self.get_open_cells()
    
    def get_open_cells(self):
        return [(i,j) for i, row in enumerate(self.maze) for j, cell in enumerate(row) if cell == 0]

    def generate_maze(self):
        pass
    
    def get_neighbors(self, cell):
        pass
    
    def __str__(self):
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.maze)
