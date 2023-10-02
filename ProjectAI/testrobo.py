import random

def get_neighbours(curr, size):
    x,y = curr
    neighbors = [(x, y + 1),(x, y - 1),(x + 1, y),(x -1, y)]
    return [(xi,yi) for xi,yi in neighbors if 0 <= xi < size and  0 <= yi < size]

#def get_valid_neighbors(maze, curr, size):

def check_dead_end(maze, cell):
    x,y = cell
    cell_neibours = get_neighbours(cell, 5)
    is_removable = []
    for i in cell_neibours:
        xi,yi = i
        if maze[xi][yi] == 0:
            is_removable.append(i)
    if len(is_removable) > 1:
        return True
    return False


def generate_maze(maze, invalid_cells):
    random_col = random.randint(0, len(maze)-1)
    random_row = random.randint(0, len(maze)-1)
    maze[random_row][random_col] = 0
    curr_cell = (random_row, random_col)
    neighbors = []
    neighbors.append(curr_cell)

    while neighbors:
        curr = neighbors.pop()
        invalid_cells.add(curr)
        x,y = curr
        maze[x][y] = 0
        neighbor_list = get_neighbours(curr, 5)
        for i in neighbor_list:
            is_dead_cell = check_dead_end(maze, i)
            if i in invalid_cells:
                neighbor_list.remove(i)
            if is_dead_cell == True and i not in invalid_cells:
                neighbor_list.remove(i)
        for i in neighbor_list:
            neighbors.append(i)
    
    return maze


'''def open_maze(maze, current, size):
    neighbors = get_neighbours(current)
    x,y = current    
    maze[x][y] = 0

    for i in neighbors:'''


hil = []


Alp = [["A","B","C", "D", "E"], ["F", "G", "H", "I", "J"],[ "K", "L", "M", "N", "O"], ["P", "Q", "R", "S", "T"], ["U", "V", "W","X", "Y"]]

k = 0

cells_invalid = set()
cells_dead = set()
generated_maze = generate_maze(Alp,cells_invalid)

print(generated_maze)
