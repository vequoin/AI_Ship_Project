import random

# Define the maze size (change this to your desired size)
maze_size = 10

# Define a function to check if a cell is a dead end (you need to implement this)
def check_dead_end(maze, cell):
    # Implement your check_dead_end logic here
    pass

# Define a function to get neighbors of a cell (you need to implement this)
def get_neighbors(cell, size):
    # Implement your get_neighbors logic here
    pass

def generate_ship(ship, invalid_cells):
    size = len(ship)
    
    while True:
        random_row = random.randint(0, size - 1)
        random_col = random.randint(0, size - 1)
        
        if (random_row, random_col) not in invalid_cells:
            break
    
    neighbors = [(random_row, random_col)]

    while neighbors:
        curr = neighbors.pop()
        invalid_cells.add(curr)
        x, y = curr
        ship[x][y] = 0
        
        neighbor_list = get_neighbors(curr, size)
        
        for i in neighbor_list:
            if i not in invalid_cells and not check_dead_end(maze, i):
                neighbors.append(i)
    
    return ship

# Create a maze (a 2D list filled with 1s to represent walls)
maze = [[1 for _ in range(maze_size)] for _ in range(maze_size)]

# Create a set to keep track of invalid cells (cells where the ship cannot go)
invalid_cells = set()

# Generate the ship on the maze
ship = [[1 for _ in range(maze_size)] for _ in range(maze_size)]  # Initialize the ship grid
ship = generate_ship(ship, invalid_cells)

# Print the maze with the ship
for row in ship:
    print(" ".join(map(str, row)))
